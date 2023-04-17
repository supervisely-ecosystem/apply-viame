import supervisely as sly
import pandas as pd
import globals as g
from collections import defaultdict


def get_tag_meta_or_create(api: sly.Api, project_id: int, meta: sly.ProjectMeta, tag_meta: sly.TagMeta):
    tag_meta_existed = meta.get_tag_meta(tag_meta.name)
    if not tag_meta_existed:
        meta = meta.add_tag_meta(tag_meta)
        api.project.update_meta(project_id, meta)
        api.project.pull_meta_ids(project_id, meta)
        tag_meta = meta.get_tag_meta(tag_meta.name)
    return meta, tag_meta


def get_obj_class_or_create(api: sly.Api, project_id: int, meta: sly.ProjectMeta, class_name: str):
    geometry = sly.Rectangle
    obj_class = meta.get_obj_class(class_name)
    if not obj_class:
        meta = meta.add_obj_class(sly.ObjClass(class_name, geometry))
        api.project.update_meta(project_id, meta)
        api.project.pull_meta_ids(project_id, meta)
        obj_class = meta.get_obj_class(class_name)
    return meta, obj_class


def prune_csv(csv_file, out_path):
    with open(csv_file, "r") as f:
        lines = f.readlines()

    line = None
    with open(out_path, "w") as f:
        for line in lines:
            line = ",".join(line.strip().split(",")[:11])+"\n"
            f.write(line)

    sly.logger.debug(f"last pruned csv line: {line}")


def collect_predictions_csv(csv_file):    
    # {ds1: {img1: [preds], img2: [preds]}}
    pred_datasets = defaultdict(lambda: defaultdict(list))

    # skip comments in csv
    skiprows = 0
    with open(csv_file, "r") as f:
        first_char = f.readline()[0]
        while first_char == "#":
            first_char = f.readline()[0]
            skiprows += 1

    # read csv
    df = pd.read_csv(csv_file, header=None, skiprows=skiprows)
    assert len(df.columns) == 11

    # read input_images
    with open("input_images.txt", "r") as f:
        input_images = f.readlines()

    # parse predictions
    df_list = df.to_dict("split")["data"]
    paths_iter = iter(input_images)
    prev_name = None
    for row in df_list:
        name1 = row[1]
        if prev_name != name1:
            prev_name = name1
            path = next(paths_iter)
            splits = path.strip().split("/")
            ds, image_name = splits[-3], splits[-1]
            assert image_name == name1
        # [x1, y1, x2, y2, conf, class_name]
        pred_datasets[ds][image_name].append(row[3:7]+row[9:11][::-1])

    # to normal dict
    pred_datasets = {k: dict(v) for k, v in pred_datasets.items()}
    return pred_datasets


api = g.api

sly.Progress("Parsing predictions...", 1)

# Create project
if g.create_project:
    free_name = api.project.get_free_name(g.WORKSPACE_ID, g.output_project_name)
    api.project.clone(g.PROJECT_ID, g.WORKSPACE_ID, free_name)
    try:
        output_project_id = api.project.get_info_by_name(g.WORKSPACE_ID, free_name).id
    except AttributeError as exc:
        sly.logger.error("Error cloning project", extra=dict(
            free_name=free_name,
            output_project_name=g.output_project_name,
            project_id=g.PROJECT_ID,
            workspace_id=g.WORKSPACE_ID,
        ))
        raise exc
else:
    output_project_id = g.PROJECT_ID

# Parse csv
prune_csv("computed_detections.csv", "computed_detections_pruned.csv")
pred_datasets = collect_predictions_csv("computed_detections_pruned.csv")

# Create tag for conf
meta = sly.ProjectMeta.from_json(api.project.get_meta(output_project_id))
tag_name = "confidence"
conf_tag = sly.TagMeta(tag_name, sly.TagValueType.ANY_NUMBER, applicable_to=sly.TagApplicableTo.OBJECTS_ONLY)
meta, conf_tag = get_tag_meta_or_create(api, output_project_id, meta, conf_tag)

# Collect predictions
datasets = api.dataset.get_list(output_project_id)
anns = []
img_ids = []
for dataset in datasets:
    img_infos = api.image.get_list(dataset.id)
    for img_info in img_infos:
        image_name = img_info.name
        try:
            preds = pred_datasets[dataset.name][image_name]
        except:
            sly.logger.warn(f"prediction not found for image {image_name}")
            continue
        labels = []
        for pred in preds:
            x1,y1,x2,y2,conf,class_name = pred
            if conf < g.threshold:
                continue
            meta, obj_class = get_obj_class_or_create(api, output_project_id, meta, class_name)
            label = sly.Label(sly.Rectangle(y1,x1,y2,x2), obj_class, [sly.Tag(conf_tag, conf)])
            labels.append(label)
        
        ann = sly.Annotation([img_info.height, img_info.width], labels)
        # ann = ann.crop_labels(sly.Rectangle(0,0, img_info.height, img_info.width))

        anns.append(ann)
        img_ids.append(img_info.id)

print("Uploading annotations...")
progress = sly.Progress("Uploading annotations...", total_cnt=len(img_ids))
if not g.create_project:
    # append labels to the existed project
    for img_id, ann in zip(img_ids, anns):
        # sdk issue: this won't append confidence tag
        api.annotation.append_labels(img_id, ann.labels, skip_bounds_validation=True)
        progress.iter_done()
else:
    for img_id, ann in zip(img_ids, anns):
        api.annotation.upload_ann(img_id, ann, skip_bounds_validation=True)
        progress.iter_done()

if sly.env.task_id(False):
    task_id = sly.env.task_id()
    api.task.set_output_project(task_id, output_project_id)
