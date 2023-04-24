import imageio
from tkinter import *
import pickle
from PIL import ImageTk, Image, ImageDraw
import PIL
import numpy as np
import pyscreenshot as ImageGrab
import io


class App(object):
    def __init__(self):
        self.window = Tk()
        self.window.title('Sketchbook')
        self.window.geometry('500x500')
        self.my_canvas = Canvas(self.window, width=500, height=500, bg='white')

        self.number_label = Label(self.window, text='PREDICTED: NONE')

        self.number_label.place(relx=0.0, rely=1.0, anchor='sw')
        self.my_canvas.pack()

        self.setup()
        self.load_model('./model.pkl')
        self.window.mainloop()

    def setup(self):
        self.my_canvas.bind("<Button-1>", self.initial_cordinates)
        self.my_canvas.bind("<B1-Motion>", self.draw)
        self.my_canvas.bind("<Button-3>", self.clear_sketchbook)
        self.my_canvas.bind("<Button-2>", self.predict_number)

    def initial_cordinates(self, event):
        global x_cord, y_cord
        self.x_cord, self.y_cord = event.x, event.y

    def draw(self, event):
        global x_cord, y_cord
        self.my_canvas.create_line((self.x_cord, self.y_cord, event.x, event.y),
                                   fill='black', width=8)
        self.x_cord, self.y_cord = event.x, event.y

    def clear_sketchbook(self, event):
        self.my_canvas.delete('all')
        self.number_label.config(text='PREDICTED: NONE')

    def load_model(self, model_path):
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        return self.model

    def predict_number(self, event):
        self.canvas_postscript = self.my_canvas.postscript(colormode='color')
        self.image = Image.open(io.BytesIO(
            self.canvas_postscript.encode('utf-8')))
        self.image = self.image.resize((8, 8))
        # Convert to grayscale
        self.image = self.image.convert('L')
        self.image = np.array(self.image)
        self.image = self.image.reshape([1, 64])
        self.prediction = self.model.predict(self.image)
        # self.label = np.argmax(self.prediction, axis=1)
        self.number_label.config(text='PREDICTED:' + str(self.prediction))


if __name__ == '__main__':
    App()
