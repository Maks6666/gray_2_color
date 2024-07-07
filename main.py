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


class Colorizer:
    def __init__(self):
        ...


    def search_4_model(self):
        t_dir = os.getcwd()
        for file in os.listdir(t_dir):
            if file.endswith(".h5"):
                model = load_model(file, compile=False)
                return model 
            
    def choises(self):
        while True:
            choises = int(input("How many pictures you want to colorize? "))
            if type(choises) == int:
                break
            else:
                choises = int(input("How many pictures you want to colorize? "))

        return choises
        

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
    

    def check_file(self, folder):
        for file in folder:
            try:
                with Image.open(file) as img:
                    img.verify()  # Проверка целостности изображения
                return True
            except (IOError, SyntaxError) as e:
                return False
    

    def img_preprocessing(self, selected_files):
        arr = []
        img_sizes = []
        for i in selected_files:
            with Image.open(i) as img:
                orig_size = img.size
                img_sizes.append(orig_size)
                img = img.convert('RGB')
                img = img.resize((240, 240))
                img_array = np.array(img)
                img_array = img_array.astype('float32') / 255.0
                    
                img_array = img_array.reshape(-1, 240, 240, 3)

                arr.append(img_array)

        return arr, img_sizes

    def model_prediction(self, model, arr, orig_size, files_fin):
        for el, file, size in zip(arr, files_fin, orig_size):
            res = model.predict(el)[0]
            img = Image.fromarray((res*255).astype('uint8'))
            img_resized = img.resize(size, Image.LANCZOS)
            img_resized.save(os.path.join(os.getcwd(), "c_" + file))
            
            




if __name__ == '__main__':

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

    if colorizer.check_file(files_list):

        img_array, img_sizes = colorizer.img_preprocessing(files_list)
        model = colorizer.search_4_model()
        colorizer.model_prediction(model, img_array, img_sizes, files_list)




    