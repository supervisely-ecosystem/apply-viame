# set -e

# env > env_state.txt

PATH_=$PATH

echo $(which python3)
echo "supervisely installed?"
echo $(python3 -m pip list | grep sup)

echo "----ENV----"
env
echo "----ENV----"

python3 src/download_project.py
echo $(cat "input_images.txt")

python3 src/get_pipe.py
PIPE=$(cat "pipe.txt")
echo $PIPE

### VIAME
export VIAME_INSTALL="/opt/noaa/viame"
source ${VIAME_INSTALL}/setup_viame.sh
kwiver runner ${VIAME_INSTALL}/configs/pipelines/${PIPE} \
    -s input:video_filename=input_images.txt
### END VIAME

# Restore environment state from the file
# source env_state.txt
export PATH=$PATH_
unset PYTHON_LIBRARY
unset PYTHONPATH

echo $(which python3)

# parse csv, export
python3 src/parse_csv.py

# kwiver runner ${VIAME_INSTALL}/configs/pipelines/detector_arctic_seal_eo_yolo.pipe \
            #   -s input:video_filename=input_image_list_seal_eo.txt