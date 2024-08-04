import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import requests
import tempfile
import os
from ffpyplayer.player import MediaPlayer

# Get video (Buffer with temp) 
VIDEO_URL = 'https://drive.google.com/uc?export=download&id=1Ok4_IemwVUfV4rls8DPy_H9JHiDJo32z'

def download_video(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Temp File
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        
        # Write temp
        with open(tmp_file.name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    
        return tmp_file.name
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not download video: {e}")
        return None

def on_button_click():
    progress_bar.grid(row=3, column=0, pady=20, sticky='ew')
    progress_bar.start(20)  
    root.after(2000, progress_bar.stop)  
    root.after(2200, play_video)  

def play_video():
    video_path = download_video(VIDEO_URL)
    if not video_path:
        return

    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video file.")
        return

    def show_frame():
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
          
            frame = cv2.resize(frame, (300, 500))
            
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)
            video_label.after(20, show_frame)  
            
            if val != 'eof' and audio_frame is not None:
                img, t = audio_frame
                
        else:
            cap.release()
            player.close_player()
            os.remove(video_path)  

    video_label.grid(row=4, column=0, pady=20, sticky='ew')
    show_frame()

root = tk.Tk()
root.title("Surprise for her")
root.geometry("350x750")
root.configure(bg='#f9f3e7')

root.grid_columnconfigure(0, weight=1)

message_label = tk.Label(root, text="Hi, I have a surprise for you", font=("Helvetica", 16), bg='#f9f3e7')
message_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

surprise_button = tk.Button(root, text="If you want to find your keys, Click Here", font=("Helvetica", 12), command=on_button_click)
surprise_button.grid(row=1, column=0, pady=20, sticky='ew')

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
progress_bar.grid(row=3, column=0, pady=20, sticky='ew')
progress_bar.grid_remove()  # Hide the progress bar initially

video_label = tk.Label(root)
video_label.grid(row=4, column=0, pady=20, sticky='ew')
video_label.grid_remove() 

root.mainloop()
