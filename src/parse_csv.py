import supervisely as sly
import pandas as pd

df = pd.read_csv("computed_detections.csv")

df.to_csv("pred.csv")