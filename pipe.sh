# PIPE=detector_fish_without_motion.pipe
# PIPE="detector_sefsc_bw_species_v2.4m_0.5x.pipe"
PIPE=detector_habcam_test_yolo_only.pipe

rm computed_detections.csv
export VIAME_INSTALL="/opt/noaa/viame"
source ${VIAME_INSTALL}/setup_viame.sh
kwiver runner ${VIAME_INSTALL}/configs/pipelines/${PIPE} \
    -s input:video_filename=input_images.txt