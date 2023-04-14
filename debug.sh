# set -e

# TODO: debug
export WORKSPACE_ID=662
export PROJECT_ID=16080

PATH_=$PATH

echo $(which python3)
echo "supervisely installed?"
echo $(python3 -m pip list | grep supervisely)

echo "----ENV----"
# env
echo "----ENV----"

python3 src/download_project.py
echo $(cat "input_images.txt")

# python3 src/get_pipe.py
PIPE=$(env | grep modal.state.viame_pipeline | cut -d= -f2)

if [[ -z "$PIPE" ]]; then
    PIPE="detector_sefsc_bw_species_v2.4m_0.5x.pipe"
fi

echo $PIPE

### VIAME
rm computed_detections.csv
export VIAME_INSTALL="/opt/noaa/viame"
source ${VIAME_INSTALL}/setup_viame.sh
kwiver runner ${VIAME_INSTALL}/configs/pipelines/${PIPE} \
    -s input:video_filename=input_images.txt
### END VIAME

# Restore environment state from the file
export PATH=$PATH_
unset PYTHON_LIBRARY
unset PYTHONPATH

echo $(which python3)

# parse csv, export
python3 src/upload_predictions.py
