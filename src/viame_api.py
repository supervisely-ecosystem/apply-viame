import subprocess
import os

print(os.getcwd())

def run_pipe(pipe_file: str, img_list: list):
    input_images_file = "input_images.txt"
    dump_image_list(img_list, path=input_images_file)

    # viame_path = "/opt/noaa/viame"
    # setup_viame_path = os.path.join(viame_path, "setup_viame.sh")
    # subprocess.call(["sh", "."+setup_viame_path])

    pipes_path = "configs/pipelines"
    cmd = f"kwiver runner {pipes_path}/{pipe_file} -s input:video_filename={input_images_file}"
    subprocess.call(cmd.split(" "))


def dump_image_list(img_list, path="input_images.txt"):
    with open(path, "w") as f:
        f.write("\n".join(img_list))

images = [
    "input_images/image_01.jpg",
    "input_images/image_02.jpg",
    ]

run_pipe("detector_fish_without_motion.pipe", images)
