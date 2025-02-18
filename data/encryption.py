import base64
import os
from data.cache_data import write_to_file


class AssetEncryptor:
    def __init__(self):
        self.assets_folder = './assets'

    def encryption_logo(self):
        """Hàm mã hóa ảnh logo"""
        image_folder = os.path.join(self.assets_folder, 'other_images')
        try:
            content = "other_images = {\n"
            for image_file in os.listdir(image_folder):
                if image_file.endswith(('.png', '.jpg', '.jpeg')):
                    piece_name = image_file.split('.')[0]

                    with open(os.path.join(image_folder, image_file), 'rb') as img:
                        encoded_string = base64.b64encode(img.read()).decode('utf-8')
                        content += f'    "{piece_name}": "{encoded_string}",\n'
            content += "}\n"

            write_to_file('data/logo.py', content)
            print("Mã hóa ảnh hoàn tất và đã lưu vào other_images.py!")
        except Exception as e:
            print(f"Xảy ra lỗi: {e}")

    def encryption_images(self):
        """Hàm mã hóa ảnh quân cờ"""
        image_folder = os.path.join(self.assets_folder, 'images')
        try:
            content = "images = {\n"
            for image_file in os.listdir(image_folder):
                if image_file.endswith(('.png', '.jpg', '.jpeg')):
                    piece_name = image_file.split('.')[0]

                    with open(os.path.join(image_folder, image_file), 'rb') as img:
                        encoded_string = base64.b64encode(img.read()).decode('utf-8')
                        content += f'    "{piece_name}": "{encoded_string}",\n'
            content += "}\n"

            write_to_file('data/image.py', content)
            print("Mã hóa ảnh hoàn tất và đã lưu vào image.py!")
        except Exception as e:
            print(f"Xảy ra lỗi: {e}")

    def encryption_sounds(self):
        """Hàm mã hóa âm thanh"""
        sound_folder = os.path.join(self.assets_folder, 'sounds')
        try:
            content = "sounds = {\n"
            for sound_file in os.listdir(sound_folder):
                if sound_file.endswith(('.wav', '.ogg', '.mp3')):
                    sound_name = sound_file.split('.')[0]

                    with open(os.path.join(sound_folder, sound_file), 'rb') as snd:
                        encoded_string = base64.b64encode(snd.read()).decode('utf-8')
                        content += f'    "{sound_name}": "{encoded_string}",\n'
            content += "}\n"

            write_to_file('data/sound.py', content)
            print("Mã hóa âm thanh hoàn tất và đã lưu vào sound.py!")
        except Exception as e:
            print(f"Xảy ra lỗi: {e}")

    def encryption_video(self):
        """Hàm mã hóa video"""
        video_folder = os.path.join(self.assets_folder, 'videos')
        try:
            content = "videos = {\n"
            for video_file in os.listdir(video_folder):
                if video_file.endswith('.mp4'):
                    video_name = video_file.split('.')[0]

                    with open(os.path.join(video_folder, video_file), 'rb') as vid:
                        encoded_string = base64.b64encode(vid.read()).decode('utf-8')
                        content += f'    "{video_name}": "{encoded_string}",\n'
            content += "}\n"

            write_to_file('data/video.py', content)
            print("Mã hóa video hoàn tất và đã lưu vào video.py!")
        except Exception as e:
            print(f"Xảy ra lỗi: {e}")

    def encryption_fonts(self):
        """Hàm mã hóa phông chữ"""
        font_file = os.path.join(self.assets_folder, 'fonts', 'FontCustom.ttf')
        try:
            content = "fonts = {\n"
            font_name = os.path.basename(font_file).split('.')[0]
            with open(font_file, 'rb') as font:
                encoded_string = base64.b64encode(font.read()).decode('utf-8')
                content += f'    "{font_name}": "{encoded_string}",\n'
            content += "}\n"

            write_to_file('data/font.py', content)
            print("Mã hóa font chữ hoàn tất và đã lưu vào font.py!")
        except Exception as e:
            print(f"Xảy ra lỗi: {e}")

    def encrypt_all(self):
        """Hàm mã hóa tất cả các loại tài nguyên"""
        self.encryption_logo()
        self.encryption_images()
        self.encryption_sounds()
        self.encryption_video()
        self.encryption_fonts()


if __name__ == '__main__':
    encryptor = AssetEncryptor()
    encryptor.encrypt_all()