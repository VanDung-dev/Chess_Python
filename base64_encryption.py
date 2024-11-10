from base64_data import images, sounds, videos, fonts
from moviepy.editor import VideoFileClip
import io
import base64
import os
import pygame
import atexit  # Thư viện để xóa file tạm khi chương trình kết thúc

# Khởi tạo pygame
pygame.init()

# Danh sách lưu các file font tạm để xóa khi kết thúc
temp_font_files = []


# Hàm thay thế hoặc chèn vào tệp mã hóa nếu tệp đã tồn tại
def append_to_file(filename, content):
    try:
        with open(filename, 'a') as python_file:  # Mở tệp ở chế độ append
            python_file.write(content)
    except Exception as e:
        print(f"Xảy ra lỗi khi ghi vào {filename}: {e}")


# Kiểm tra sự tồn tại của tệp mã hóa
def file_exists(filename):
    return os.path.exists(filename)


def encode_images():
    image_folder = 'images'  # Thư mục chứa ảnh
    try:
        content = "images = {\n"
        for image_file in os.listdir(image_folder):
            if image_file.endswith(('.png', '.jpg', '.jpeg')):
                piece_name = image_file.split('.')[0]

                with open(os.path.join(image_folder, image_file), 'rb') as img:
                    encoded_string = base64.b64encode(img.read()).decode('utf-8')
                    content += f'    "{piece_name}": "{encoded_string}",\n'
        content += "}\n"

        if not file_exists('base64_data/images.py'):
            with open('base64_data/images.py', 'w') as python_file:
                python_file.write(content)
            print("Mã hóa ảnh hoàn tất và đã lưu vào images.py!")
        else:
            append_to_file('base64_data/images.py', content)  # Chèn vào tệp nếu đã tồn tại
            print("Đã thêm bản mã hóa ảnh mới vào images.py!")
    except Exception as e:
        print(f"Xảy ra lỗi: {e}")


def encode_sounds():
    sound_folder = 'sounds'  # Thư mục chứa âm thanh
    try:
        content = "sounds = {\n"
        for sound_file in os.listdir(sound_folder):
            if sound_file.endswith(('.wav', '.ogg', '.mp3')):
                sound_name = sound_file.split('.')[0]

                with open(os.path.join(sound_folder, sound_file), 'rb') as snd:
                    encoded_string = base64.b64encode(snd.read()).decode('utf-8')
                    content += f'    "{sound_name}": "{encoded_string}",\n'
        content += "}\n"

        if not file_exists('base64_data/sounds.py'):
            with open('base64_data/sounds.py', 'w') as python_file:
                python_file.write(content)
            print("Mã hóa âm thanh hoàn tất và đã lưu vào sounds.py!")
        else:
            append_to_file('base64_data/sounds.py', content)  # Chèn vào tệp nếu đã tồn tại
            print("Đã thêm bản mã hóa âm thanh mới vào sounds.py!")
    except Exception as e:
        print(f"Xảy ra lỗi: {e}")


def encode_video():
    video_folder = 'videos'  # Thư mục chứa video
    try:
        content = "videos = {\n"
        for video_file in os.listdir(video_folder):
            if video_file.endswith('.mp4'):
                video_name = video_file.split('.')[0]

                with open(os.path.join(video_folder, video_file), 'rb') as vid:
                    encoded_string = base64.b64encode(vid.read()).decode('utf-8')
                    content += f'    "{video_name}": "{encoded_string}",\n'
        content += "}\n"

        if not file_exists('base64_data/videos.py'):
            with open('base64_data/videos.py', 'w') as python_file:
                python_file.write(content)
            print("Mã video hoàn tất và được lưu vào videos.py!")
        else:
            append_to_file('base64_data/videos.py', content)  # Chèn vào tệp nếu đã tồn tại
            print("Đã thêm bản mã hóa video mới vào videos.py!")
    except Exception as e:
        print(f"Xảy ra lỗi: {e}")


def encode_fonts():
    font_file = 'fonts/FontCustom.ttf'  # Đường dẫn font chữ
    try:
        content = "fonts = {\n"
        font_name = os.path.basename(font_file).split('.')[0]
        with open(font_file, 'rb') as font:
            encoded_string = base64.b64encode(font.read()).decode('utf-8')
            content += f'    "{font_name}": "{encoded_string}",\n'
        content += "}\n"

        if not file_exists('base64_data/fonts.py'):
            with open('base64_data/fonts.py', 'w') as python_file:
                python_file.write(content)
            print("Mã hóa font chữ hoàn tất và đã lưu vào fonts.py!")
        else:
            append_to_file('base64_data/fonts.py', content)  # Chèn vào tệp nếu đã tồn tại
            print("Đã thêm bản mã hóa font chữ mới vào fonts.py!")
    except Exception as e:
        print(f"Xảy ra lỗi: {e}")


# Tạo thư mục cache tạm thời
def get_cache_dir():
    """Trả về đường dẫn thư mục cache, tạo thư mục nếu chưa tồn tại."""
    if os.name == 'nt':  # Windows
        cache_dir = 'C:/.cache_python'
    else:  # Linux và macOS
        cache_dir = os.path.join(os.getenv("HOME"), ".cache_python")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def decrypt_image(piece, size):
    """Giải mã và tải ảnh của quân cờ, điều chỉnh kích thước"""
    if isinstance(images[piece], str):  # Nếu ảnh là chuỗi base64_data
        image_data = base64.b64decode(images[piece])
        image_file = io.BytesIO(image_data)
        image = pygame.image.load(image_file)
    else:
        image = images[piece]

    return pygame.transform.smoothscale(image, size)


def decrypt_sound(sound_name):
    """Hàm phát âm thanh từ dữ liệu đã mã hóa"""
    pygame.mixer.init()
    sound_data = base64.b64decode(sounds[sound_name])
    sound_file = io.BytesIO(sound_data)
    sound = pygame.mixer.Sound(sound_file)
    sound.play()


def decrypt_video(video_name):
    """Hàm phát video từ dữ liệu đã mã hóa"""
    global clip
    cache_dir = get_cache_dir()
    temp_video_path = os.path.join(cache_dir, 'temp.mp4')

    try:
        os.makedirs(cache_dir, exist_ok=True)
        video_bytes = base64.b64decode(videos[video_name])
        with open(temp_video_path, 'wb') as output_file:
            output_file.write(video_bytes)
        clip = VideoFileClip(temp_video_path)
        clip.preview()
    finally:
        clip.close()
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)


def decrypt_font(font_name):
    """Giải mã font từ dữ liệu đã mã hóa và trả về đường dẫn file tạm để sử dụng trong pygame."""
    font_data = base64.b64decode(fonts[font_name])
    cache_dir = get_cache_dir()
    temp_font_path = os.path.join(cache_dir, f"{font_name}.ttf")

    os.makedirs(cache_dir, exist_ok=True)

    # Ghi dữ liệu font vào file tạm nếu chưa tồn tại
    if not os.path.exists(temp_font_path):
        with open(temp_font_path, "wb") as temp_font_file:
            temp_font_file.write(font_data)
        temp_font_files.append(temp_font_path)

    return temp_font_path


# Đăng ký hàm xóa file tạm khi chương trình kết thúc
@atexit.register
def cleanup_temp_fonts():
    for font_path in temp_font_files:
        if os.path.exists(font_path):
            os.remove(font_path)


if __name__ == '__main__':
    encode_images()
    encode_sounds()
    encode_video()
    encode_fonts()
