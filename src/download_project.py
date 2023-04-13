import os
import supervisely as sly
import globals as g
import shutil

def dump_image_list(img_list, path="input_images.txt"):
    with open(path, "w") as f:
        f.write("\n".join(img_list))

project_path = "input_project"
if os.path.exists(project_path):
    shutil.rmtree(project_path)

sly.download_project(g.api, g.PROJECT_ID, project_path, batch_size=50)

project = sly.Project(project_path, sly.OpenMode.READ)

imgs = []
for dataset in project.datasets:
    dataset: sly.Dataset
    items = dataset.get_items_names()
    for item in items:
        imgs.append(dataset.get_img_path(item))

dump_image_list(imgs, path="input_images.txt")