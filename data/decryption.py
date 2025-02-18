import cv2
import io
import os
import re
import base64
import pygame
from data import images, sounds, videos, fonts, other_images
from data.cache_data import get_cache_dir, temp_font_files


def decryption_logo(logo, size):
    """Giải mã và tải ảnh của quân cờ, điều chỉnh kích thước"""
    if isinstance(other_images[logo], str):
        image_data = base64.b64decode(other_images[logo])
        image_file = io.BytesIO(image_data)
        image = pygame.image.load(image_file)
    else:
        image = other_images[logo]

    return pygame.transform.smoothscale(image, size)


def decryption_image(piece, size):
    """Giải mã ảnh và lưu vào file tạm thời, loại bỏ số cuối trong tên quân cờ."""

    # Loại bỏ số cuối tên quân cờ
    piece_name = re.sub(r'\d+$', '', piece)

    if isinstance(images.get(piece), str):
        try:
            image_data = base64.b64decode(images[piece])
            image_file = io.BytesIO(image_data)
            image = pygame.image.load(image_file)
        except Exception as e:
            print(f"Không thể giải mã ảnh cho {piece}: {e}")
            return None
    else:
        image = images.get(piece)

    # Điều chỉnh kích thước ảnh
    image = pygame.transform.smoothscale(image, size)

    # Lưu ảnh vào file tạm trong thư mục cache
    temp_image_path = os.path.join(get_cache_dir(), f"{piece_name}.png")
    pygame.image.save(image, temp_image_path)  # Lưu ảnh vào file tạm

    return temp_image_path  # Trả về đường dẫn tới file tạm thời


def decryption_sound(sound_name):
    """Hàm phát âm thanh từ dữ liệu đã mã hóa"""
    pygame.mixer.init()
    sound_data = base64.b64decode(sounds[sound_name])
    sound_file = io.BytesIO(sound_data)
    sound = pygame.mixer.Sound(sound_file)
    sound.play()


def decryption_video(video_name):
    """Hàm phát video từ dữ liệu đã mã hóa"""
    global clip
    cache_dir = get_cache_dir()
    temp_video_path = os.path.join(cache_dir, 'temp.mp4')

    os.makedirs(cache_dir, exist_ok=True)
    video_bytes = base64.b64decode(videos[video_name])
    with open(temp_video_path, 'wb') as output_file:
        output_file.write(video_bytes)
    cap = cv2.VideoCapture(temp_video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            pass

    cap.release()
    cv2.destroyAllWindows()


def decryption_font(font_name):
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