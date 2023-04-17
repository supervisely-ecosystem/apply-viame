PATH_=$PATH

# grep pipe form env
PIPE=$(env | grep modal.state.viame_pipeline | cut -d= -f2)
echo $PIPE

# Download project
python3 src/download_project.py

### Apply VIAME
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
