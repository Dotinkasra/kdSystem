from base64 import encode
import subprocess
import os
import shutil
import urllib
import io

class Waifu2x():
    def do(self, image: str) -> str:
        save_dir = "./static/waifu2x/"
        upscale_image = image + "2x.png"
        cmd = [
            "./modules/realesrgan-ncnn-vulkan/realesrgan-ncnn-vulkan",
             "-m", "./modules/realesrgan-ncnn-vulkan/models",
             "-i", save_dir + image,
             "-n", "realesrgan-x4plus-anime",
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

class Erocool():
    def do(self, url: str) -> str:
        save_dir = "./static/waifu2x/"
        cmd = [
            "./modules/bin/erocoolAPI", url,
            "-o", save_dir
        ]
        try:
            result = subprocess.Popen(cmd, stdout = subprocess.PIPE)
            result.wait()

            if not result.returncode == 0:
                return 
            stdout = str(result.stdout.readline().decode('utf-8')).rstrip(os.linesep)
            encode_file_name = urllib.parse.quote(os.path.basename(stdout).replace('/', '_'))
            if len(encode_file_name) >= 200:
                encode_file_name = encode_file_name[:200]

            zip_path = (f"{save_dir}{encode_file_name}")

            shutil.make_archive(
                zip_path,
                format = 'zip',
                root_dir = stdout
            )
            return f"{zip_path}.zip"
        except Exception as e:
            print(e)
            return
        finally:
            #shutil.rmtree(stdout)
            pass

class YouTube():
    def do(self, url: str, audio_only: bool) -> str:
        fmt = "bestaudio" if audio_only else "bestvideo+bestaudio" 
        save_dir = "./static/server/"
        cmd = [
            "yt-dlp",
            "-f", fmt,
            url,
            "-x", "-v", 
            "--audio-quolity", "0",
            "--embed-thumbnail",
            "--add-metadata"
        ]
        try:
            result = subprocess.Popen(cmd, stdout = subprocess.PIPE)
            result.wait()

            if not result.returncode == 0:
                return 
            stdout = str(result.stdout.readline().decode('utf-8')).rstrip(os.linesep)
            zip_path = f"{save_dir}{os.path.basename(stdout).replace('/', '_')}"
            shutil.make_archive(
                zip_path,
                format = 'zip',
                root_dir = stdout
            )
            print("保存完了")
            return f"{zip_path}.zip"
        except:
            return
        finally:
            shutil.rmtree(stdout)
        