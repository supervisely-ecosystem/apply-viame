import os
import supervisely as sly
from supervisely.project.download import download_async_or_sync
import globals as g
import shutil

def dump_image_list(img_list, path="input_images.txt"):
    with open(path, "w") as f:
        f.write("\n".join(img_list))

project_path = "input_project"
if os.path.exists(project_path):
    shutil.rmtree(project_path)

dataset_ids = None
if isinstance(g.DATASET_ID, int):
    dataset_ids = [g.DATASET_ID]

download_async_or_sync(g.api, g.PROJECT_ID, project_path, dataset_ids=dataset_ids, batch_size=50, log_progress=True)

project = sly.Project(project_path, sly.OpenMode.READ)

imgs = []
for dataset in project.datasets:
    dataset: sly.Dataset
    items = dataset.get_items_names()
    for item in items:
        imgs.append(dataset.get_img_path(item))

dump_image_list(imgs, path="input_images.txt")

sly.Progress("Model inference...", total_cnt=1)
