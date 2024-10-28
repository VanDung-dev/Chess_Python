from images import images
from sounds import sounds
from videos import videos
from moviepy.editor import VideoFileClip
import base64
import os
import io
import pygame

def decrypt_image(piece, size):
    """Giải mã và tải ảnh của quân cờ, điều chỉnh kích thước"""
    if isinstance(images[piece], str):  # Nếu ảnh là chuỗi base64
        image_data = base64.b64decode(images[piece])
        image_file = io.BytesIO(image_data)
        image = pygame.image.load(image_file)
    else:
        image = images[piece]

    # Thay đổi kích thước ảnh theo kích thước mong muốn (size)
    return pygame.transform.smoothscale(image, size)

# Giải mã âm thanh và phát âm
def decrypt_sound(sound_name):
    """Hàm phát âm thanh từ dữ liệu đã mã hóa"""
    pygame.mixer.init()

    # Giải mã âm thanh
    sound_data = base64.b64decode(sounds[sound_name])
    sound_file = io.BytesIO(sound_data)  # Tạo stream từ dữ liệu đã giải mã
    sound = pygame.mixer.Sound(sound_file)  # Tải âm thanh từ stream
    sound.play()

def decrypt_image(piece, size):
    """Giải mã và tải ảnh của quân cờ, điều chỉnh kích thước"""
    if isinstance(images[piece], str):  # Nếu ảnh là chuỗi base64
        image_data = base64.b64decode(images[piece])
        image_file = io.BytesIO(image_data)
        image = pygame.image.load(image_file)
    else:
        image = images[piece]

    # Thay đổi kích thước ảnh theo kích thước mong muốn (size)
    return pygame.transform.smoothscale(image, size)

# Giải mã âm thanh và phát âm
def decrypt_sound(sound_name):
    """Hàm phát âm thanh từ dữ liệu đã mã hóa"""
    pygame.mixer.init()

    # Giải mã âm thanh
    sound_data = base64.b64decode(sounds[sound_name])
    sound_file = io.BytesIO(sound_data)  # Tạo stream từ dữ liệu đã giải mã
    sound = pygame.mixer.Sound(sound_file)  # Tải âm thanh từ stream
    sound.play()


# Giải mã video
def decrypt_video(video_name):
    """Hàm phát video từ dữ liệu đã mã hóa"""
    cache_dir = 'C:/cache'  # Đường dẫn thư mục tạm thời chỉ áp dụng với Windows
    temp_video_path = os.path.join(cache_dir, 'temp.mp4')  # Đường dẫn file video tạm thời

    try:
        os.makedirs(cache_dir, exist_ok=True)
        video_bytes = base64.b64decode(videos[video_name])
        with open(temp_video_path, 'wb') as output_file:
            output_file.write(video_bytes)
        clip = VideoFileClip(temp_video_path)
        clip.preview()
    finally:
        # Đảm bảo video được đóng
        clip.close()
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if os.path.exists(cache_dir):
            os.rmdir(cache_dir)


