import supervisely as sly
import os


api = sly.Api.from_env()

TEAM_ID = int(sly.env.team_id())
WORKSPACE_ID = int(sly.env.workspace_id())

PROJECT_ID = sly.env.project_id(raise_not_found=False)
DATASET_ID = sly.env.dataset_id(raise_not_found=False)

merge_predictions = os.getenv("modal.state.merge_predictions")
output_project_name = os.getenv("modal.state.output_project_name")
if not output_project_name:
    output_project_name = f"{api.project.get_info_by_id(PROJECT_ID).name} predicted"
viame_pipeline = os.getenv("modal.state.viame_pipeline")
threshold = os.getenv("modal.state.threshold")

if not threshold:
    print("DEBUG:::not threshold")
    threshold = 0.1
else:
    threshold = float(threshold)
    print("OK. Remove this in globals.py")