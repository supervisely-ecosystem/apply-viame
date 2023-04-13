import supervisely as sly
import pandas as pd
import globals as g
from collections import defaultdict

def get_tag_meta_or_create(api: sly.Api, project_id: int, meta: sly.ProjectMeta, tag_meta: sly.TagMeta):
    tag_meta = meta.get_tag_meta(tag_meta.name)
    if not tag_meta:
        meta = meta.add_tag_meta(tag_meta)
        api.project.update_meta(project_id, meta)
        api.project.pull_meta_ids(project_id, meta)
        tag_meta = meta.get_tag_meta(image_name)
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


def collect_predictions_csv():    
    # {ds1: {img1: [preds], img2: [preds]}}
    pred_datasets = defaultdict(lambda: defaultdict(list))

    # skip comments in csv
    skiprows = 0
    with open("computed_detections.csv", "r") as f:
        first_char = f.readline()[0]
        while first_char == "#":
            first_char = f.readline()[0]
            skiprows += 1

    # read csv
    df = pd.read_csv("computed_detections.csv", header=None, skiprows=skiprows)
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
        pred_datasets[ds][image_name].append(row[3:8]+[row[9]])

    # to normal dict
    pred_datasets = {k: dict(v) for k, v in pred_datasets.items()}
    return pred_datasets

api = g.api

if not g.merge_predictions:
    free_name = api.project.get_free_name(g.WORKSPACE_ID, g.output_project_name)
    api.project.clone(g.PROJECT_ID, g.WORKSPACE_ID, free_name)
    output_project_id = api.project.get_info_by_name(g.WORKSPACE_ID, free_name).id
else:
    output_project_id = g.PROJECT_ID

dsid = api.dataset.get_list(output_project_id)[0].id
print(f"https://dev.supervise.ly/app/images/440/662/{output_project_id}/{dsid}")

pred_datasets = collect_predictions_csv()
# print(pred_datasets)

# TODO: debug
# output_project_id = 16080

meta = sly.ProjectMeta.from_json(api.project.get_meta(output_project_id))

tag_name = "confidence"
conf_tag = sly.TagMeta(tag_name, sly.TagValueType.ANY_NUMBER, applicable_to=sly.TagApplicableTo.OBJECTS_ONLY)
meta, conf_tag = get_tag_meta_or_create(api, output_project_id, meta, conf_tag)

datasets = api.dataset.get_list(output_project_id)
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
        api.annotation.append_labels(img_info.id, labels, True)
