FROM kitware/viame-worker:latest

USER root

RUN pip3 install supervisely==6.73.290

# add addons
WORKDIR /opt/noaa/viame
COPY HabCam_Models .
COPY VIAME-SEFSC-Models .
