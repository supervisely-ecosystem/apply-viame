# set -e

# debug
export WORKSPACE_ID=662
export PROJECT_ID=20025

PATH_=$PATH

echo $(which python3)
echo "supervisely installed?"
echo $(python3 -m pip list | grep supervisely)

PIPE=$(env | grep modal.state.viame_pipeline | cut -d= -f2)

if [[ -z "$PIPE" ]]; then
    # debug
    rm computed_detections.csv
    PIPE="detector_habcam_test_yolo_only.pipe"
fi

echo $PIPE

# Download project
python3 src/download_project.py
echo $(cat "input_images.txt")

# Apply VIAME
export VIAME_INSTALL="/opt/noaa/viame"
source ${VIAME_INSTALL}/setup_viame.sh
kwiver runner ${VIAME_INSTALL}/configs/pipelines/${PIPE} \
    -s input:video_filename=input_images.txt

# Restore environment
export PATH=$PATH_
unset PYTHON_LIBRARY
unset PYTHONPATH

# Parse csv, upload
python3 src/upload_predictions.py
