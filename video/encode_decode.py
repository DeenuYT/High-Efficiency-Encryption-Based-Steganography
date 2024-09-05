from PIL import Image, ImageDraw, ImageFont
import os
from cryptography.fernet import Fernet

def encode_image(text, image_path):
    if os.path.exists(image_path):
        try:
            if text:
                image = Image.open(image_path)
                encoded_image = encode_message_in_image(image, text)
                encoded_image.save(image_path)
                # print(f"Message encoded successfully.\nimage - {image_path}\ntext - {text}")
            else:
                print("Invalid character: No text to encode.")
        except Exception as e:
            print(f"Error encoding message: {e}")
    else:
         print("Image not found.")

def get_hidden_message(image_path, key_path):
    if image_path and key_path:
        try:
            image = Image.open(image_path)
            encrypted_message = decode_message_from_image(image)
            if encrypted_message:
                # Decrypt the message using the provided key
                with open(key_path, 'rb') as key_file:
                    key = key_file.read()
                cipher_suite = Fernet(key)
                decrypted_message = cipher_suite.decrypt(encrypted_message)
                # print(f"Image - {image_path}\nEnc msg - {encrypted_message}")
                return decrypted_message
        except Exception as e:
            print(f"Error decoding message: {e}")

def encode_message_in_image(image, message):
    width, height = image.size
    encoded_image = image.copy()
    draw = ImageDraw.Draw(encoded_image)
    font = ImageFont.load_default()

    # Encode each character in the message
    x, y = 10, 10
    for byte in message:
        binary_byte = format(byte, '08b')
        for bit in binary_byte:
            pixel = list(encoded_image.getpixel((x, y)))
            pixel[-1] = int(bit)
            encoded_image.putpixel((x, y), tuple(pixel))
            x += 1
            if x >= width:
                x = 10
                y += 1
                if y >= height:
                    break
    return encoded_image

def decode_message_from_image(image):
    binary_message = bytearray()
    width, height = image.size
    x, y = 10, 10
    byte_buffer = ''
    while y < height:
        pixel = image.getpixel((x, y))
        byte_buffer += str(pixel[-1])
        if len(byte_buffer) == 8:
            binary_message.append(int(byte_buffer, 2))
            byte_buffer = ''
        x += 1
        if x >= width:
            x = 10
            y += 1
            if y >= height:
                break
    return bytes(binary_message)

# Example usage:
# encode_image(b'Hello, World!', 'example.png')
# decoded_message = get_hidden_message('example.png', 'key.key')
# print(decoded_message)
