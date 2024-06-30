import cv2
import numpy as np
from PIL import Image
import os
import time
import shutil

# Define a more granular ASCII character set (from darkest to lightest)
ASCII_CHARS = '@%#*+=-:. '

def get_terminal_size():
    columns, rows = shutil.get_terminal_size()
    return rows, columns

def resize_image(image, new_width):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Adjust for terminal character spacing
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return resized_image

def map_color_to_ascii(pixel_value):
    return ASCII_CHARS[min(pixel_value * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)]

def frame_to_ascii(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    terminal_height, terminal_width = get_terminal_size()
    image = resize_image(image, terminal_width)
    grayscale_image = image.convert('L')
    
    ascii_str = ''
    for y in range(grayscale_image.height):
        for x in range(grayscale_image.width):
            pixel_value = grayscale_image.getpixel((x, y))
            ascii_str += map_color_to_ascii(pixel_value)
        ascii_str += '\n'
    
    return ascii_str

def main():
    cap = cv2.VideoCapture(0)  # 0 for default camera
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            ascii_frame = frame_to_ascii(frame)
            
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
            print(ascii_frame, end='')
            
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
    
    except KeyboardInterrupt:
        print("Exiting...")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
