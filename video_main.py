import curses
import os
from PIL import Image
import cv2
import numpy as np

import warnings
from urllib3.exceptions import InsecureRequestWarning

import tensorflow as tf
from tensorflow import keras 
from keras.models import load_model
# unpacked model


import warnings
from urllib3.exceptions import InsecureRequestWarning

# Отключаем предупреждения InsecureRequestWarning

# if autoencoder.weights:
#     print("Model trained successfully.")

class Colorizer:
    def __init__(self):
        ...
            
    def choises(self):
        while True:
            choises = int(input("How many pictures you want to colorize? "))
            if type(choises) == int:
                break
            else:
                choises = int(input("How many pictures you want to colorize? "))

        return choises
    

    def search_4_model(self):
        t_dir = os.getcwd()
        for file in os.listdir(t_dir):
            if file.endswith(".h5"):
                model = load_model(file, compile=False)
                return model 
        

    def files_list(self, stdscr, items, num_choices):
        curses.curs_set(0)
        stdscr.clear()

        current_row = 0
        top_row = 0
        files_fin = []

        while len(files_fin) < num_choices:
            while True:
                stdscr.clear()
                for i in range(min(len(items) - top_row, curses.LINES)):
                    idx = top_row + i
                    if idx == current_row:
                        stdscr.addstr(i, 0, f"-> {items[idx]}", curses.A_REVERSE)
                    else:
                        stdscr.addstr(i, 0, f"   {items[idx]}")

                stdscr.refresh()

            
                key = stdscr.getch()

                if key == curses.KEY_UP and current_row > 0:
                    current_row -= 1
                    if current_row < top_row:
                        top_row = current_row
                elif key == curses.KEY_DOWN and current_row < len(items) - 1:
                    current_row += 1
                    if current_row >= top_row + curses.LINES:
                        top_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    files_fin.append(items[current_row])
                    del items[current_row]
                    break
                elif key == ord('\b'):
                    if files_fin:
                        item_to_return = files_fin.pop()
                        items.insert(current_row, item_to_return)
                        current_row += 1

                stdscr.refresh()

        return files_fin
    

    def check_file(self, video_path):
        video_extensions = ['.mp4', '.avi', '.mov']  # Расширения видеофайлов, которые мы поддерживаем
        _, file_extension = os.path.splitext(video_path)
        return file_extension.lower() in video_extensions
    

    def img_preprocessing(self, video_path):
        cap = cv2.VideoCapture(video_path)
        arr = []
        
    
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # set any size, depending on model input size
            frame_resized = cv2.resize(frame_rgb, (240, 240))
            frame_resized = frame_resized.astype('float32') / 255.0
            frame_resized = np.expand_dims(frame_resized, axis=0)

            frame_size = frame.size
            if frame_size:
                frame_size = frame_resized.shape[1:3]

            # Добавляем кадр в массив кадров
            arr.append(frame_resized)
            
        arr = np.array(arr)
        cap.release()

        return arr, frame_size

    def model_prediction(self, model, arr, orig_size, files_fin):

        height, width = orig_size  # распаковываем кортеж
        out = cv2.VideoWriter(f"colorized_{files_fin}", cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (width, height))
        
        for frame in arr:
            res = model.predict(frame)[0]
            res = (res * 255).astype('uint8')
            res_bgr = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            out.write(res_bgr)

        out.release()




if __name__ == '__main__':

    warnings.simplefilter('ignore', InsecureRequestWarning)

    items = os.getcwd()
    items_list = os.listdir(items)

    colorizer = Colorizer()

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # choises = colorizer.choises()

    # files_list = colorizer.files_list(stdscr, items_list, choises)

    files_list = colorizer.files_list(stdscr, items_list, 1)

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    if colorizer.check_file(files_list[0]):

        frames, size = colorizer.img_preprocessing(files_list[0])
        autoencoder = colorizer.search_4_model()
        colorizer.model_prediction(autoencoder, frames, size, files_list[0])




    