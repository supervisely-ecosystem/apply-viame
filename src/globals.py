import supervisely as sly
import os


api = sly.Api.from_env()

TEAM_ID = int(sly.env.team_id())
WORKSPACE_ID = int(sly.env.workspace_id())

PROJECT_ID = None
DATASET_ID = None

if os.environ.get("modal.state.slyProjectId") is not None:
    PROJECT_ID = int(os.environ.get("modal.state.slyProjectId"))
if os.environ.get("modal.state.slyDatasetId") is not None:
    DATASET_ID = int(os.environ.get("modal.state.slyDatasetId"))
