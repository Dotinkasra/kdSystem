import subprocess
import os

class Waifu2x():
    def do(self, image):
        save_dir = "./static/waifu2x/"
        upscale_image = image + "2x.png"
        cmd = [
            "./modules/realesrgan-ncnn-vulkan/realesrgan-ncnn-vulkan",
             "-m", "./modules/realesrgan-ncnn-vulkan/models",
             "-i", save_dir + image,
             "-s", "2",
             "-o", save_dir + upscale_image,
             "-v"
        ]
        result = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        result.wait()

        os.remove(save_dir + image)
        if result.returncode == 0:
            return upscale_image
        else:
            return ""