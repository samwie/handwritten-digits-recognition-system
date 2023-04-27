import tkinter as tk
import pickle
import io
from PIL import Image
import numpy as np


class App(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Sketchbook')
        self.window.geometry('500x500')
        self.my_canvas = tk. Canvas(
            self.window, width=500, height=500, bg='white')

        self.number_label = tk. Label(self.window, text='PREDICTED: NONE')

        self.number_label.place(relx=0.0, rely=1.0, anchor='sw')
        self.my_canvas.pack()

        self.setup()
        self.load_model('./../training/model.pkl')
        self.window.mainloop()

    def setup(self):
        self.my_canvas.bind("<Button-3>", self.clear_sketchbook)
        self.my_canvas.bind("<Button-2>", self.predict_number)
        self.my_canvas.bind("<B1-Motion>", self.draw_event)

    def draw_event(self, event):
        self.x = event.x
        self.y = event.y

        self.x1 = self.x-30
        self.y1 = self.y - 30
        self.x2 = self.x + 30
        self.y2 = self.y + 30

        self.my_canvas.create_oval(
            (self.x1, self.y1, self.x2, self.y2), fill='black')

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
        self.image = self.image.convert(mode='L')
        self.image = np.array(self.image)
        self.image = np.invert(self.image)
        self.image = self.image.reshape([1, -1])
        self.image = np.round(self.image/16.0)
        self.prediction = self.model.predict(self.image)
        self.number_label.config(text='PREDICTED:' + str(self.prediction))

if __name__ == '__main__':
    App()
