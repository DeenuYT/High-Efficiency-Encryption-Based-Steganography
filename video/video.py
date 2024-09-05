import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from .img2vid import images_to_video
from .encode_decode import encode_image, get_hidden_message
from cryptography.fernet import Fernet
import os
import shutil

class VideoSteganography:

    def __init__(self, root):
        self.root = root
        self.root.title("Video Steganography")
        self.root.geometry("800x450")
        self.root.resizable(False, False)

        # Create a style for buttons
        style = ttk.Style()
        style.configure("TButton", padding=(5, 5), font=("Helvetica", 12))

        # Custom color schemes
        style.map("TButton",
            background=[("active", "dodgerblue"), ("pressed", "cyan")],
            foreground=[("active", "white"), ("pressed", "black")]
        )
        style.configure("TLabel", font=("Helvetica", 14), foreground="blue")

        self.log = tk.Text(root, width=50, height=2)
        self.log.pack(pady=10)

        # Left side for encoding
        left_frame = tk.Frame(root)
        left_frame.pack(side="left", padx=20)

        ttk.Label(left_frame, text="Select Video to Encode:").pack()
        self.encode_button = ttk.Button(left_frame, text="Add Video", command=self.select_video)
        self.encode_button.pack(pady=10)

        ttk.Label(left_frame, text="Enter the message:").pack()
        self.text_entry = ttk.Entry(left_frame, width=40)
        self.text_entry.pack(pady=10)

        self.encode_button = ttk.Button(left_frame, text="Perform Steganography", command=self.encode_vid_data)
        self.encode_button.pack(pady=10)

        # Separator
        ttk.Separator(left_frame, orient='vertical').pack(fill='y', padx=10, pady=10, side='right')

        # Right side for decoding
        right_frame = tk.Frame(root)
        right_frame.pack(side="right", padx=20)

        ttk.Label(right_frame, text="Select Encoded Video:").pack()
        self.decode_button = ttk.Button(right_frame, text="Select Video", command=self.select_encoded_image)
        self.decode_button.pack(pady=10)

        ttk.Label(right_frame, text="Select Key:").pack()
        self.key_button = ttk.Button(right_frame, text="Select Key", command=self.select_key)
        self.key_button.pack(pady=10)

        self.get_message_button = ttk.Button(right_frame, text="Get Hidden Message", command=self.decode_vid_data)
        self.get_message_button.pack(pady=10)

        self.message_text = tk.Text(right_frame, height=5, width=40)
        self.message_text.pack(pady=10)

        self.video_path = None
        self.key_path = None
        self.key = None

    def select_video(self):
        video_path = filedialog.askopenfilename(title="Select Video to Encode")
        if video_path:
            self.video_path = video_path
            self.log.delete("1.0", tk.END)
            self.log.insert("1.0", "Video Loaded Successfully")
        else:
            self.log.delete("1.0", tk.END)
            self.log.insert("1.0", "Video selection canceled by the user")


    def select_encoded_image(self):
        self.video_path = filedialog.askopenfilename(title="Select Encoded Video")
        self.log.delete("1.0", tk.END)
        self.log.insert("1.0", "Video Added")

    def select_key(self):
        key_path = filedialog.askopenfilename(title="Select Key")
        if key_path:
            self.key_path = key_path
            with open(self.key_path, 'rb') as key_file:
                self.key = key_file.read()
                self.log.delete("1.0", tk.END)
                self.log.insert("1.0", "Key Loaded Successfully")
        else:
            self.log.delete("1.0", tk.END)
            self.log.insert("1.0", "Key selection canceled by the user")

    def extract_frames(self, video):
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")
        temp_folder = "./tmp"
        self.log.delete("1.0", tk.END)
        self.log.insert("1.0", "[INFO] tmp directory is created")
        print("[INFO] tmp directory is created")

        vidcap = cv2.VideoCapture(video)
        count = 0

        while True:
            success, image = vidcap.read()
            if not success:
                break
            cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
            count += 1
        self.log.delete("1.0", tk.END)
        self.log.insert("1.0", "Frame Extraction Successfull!!!")
        print("Frame Extraction Successfull!!!")

    def clean_tmp(self, path="./tmp"):
        if os.path.exists(path):
            shutil.rmtree(path)
            self.log.delete("1.0", tk.END)
            self.log.insert("1.0", "[INFO] tmp files are cleaned up")
            print("[INFO] tmp files are cleaned up")

    def encode_vid_data(self):
        self.extract_frames(self.video_path)
        string = self.text_entry.get()

        # Generate a key
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        
        # Encoding
        k = 0
        for i in string:
            frame = f'./tmp/{k}.png'
            encrypted_message = cipher_suite.encrypt(i.encode())
            encode_image(encrypted_message, frame)
            k += 1
        self.log.delete("1.0", tk.END)
        self.log.insert("1.0", "Encode successful")
        print("Encode successful")

        key_path = 'video/key.key'
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        self.log.delete("1.0", tk.END)
        self.log.insert("1.0", "Key Saved Successfully")
        print("Key Saved Successfully")

        images_to_video()
        self.clean_tmp()
        
    def decode_vid_data(self):
        self.extract_frames(self.video_path)
        key = self.key_path
        k = 0
        res = []  # Initialize as a list
        while True:
            try:
                frame = f'./tmp/{k}.png'
                text = get_hidden_message(frame, key)
                res.append(text.decode())  # Convert bytes to string
                k += 1
            except Exception as e:  # Handle specific exceptions if needed
                print(f"An exception occurred: {e}")
                break

        decoded_message = ''.join(res)  # Join the list into a string
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert("1.0", f"Decoded Message: {decoded_message}")
        print("Decoded Message:", decoded_message)
        self.clean_tmp()

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoSteganography(root)
    root.mainloop()
