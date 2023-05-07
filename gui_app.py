import io
import pickle
import tkinter as tk

import numpy as np
from PIL import Image


class App:
    def __init__(self, model_path="./training/model.pkl"):
        self.window = tk.Tk()
        self.window.title("Sketchbook")
        self.window.geometry("500x500")
        self.my_canvas = tk.Canvas(self.window, width=500, height=500, bg="white")

        self.number_label = tk.Label(self.window, text="PREDICTED: NONE")

        self.number_label.place(relx=0.0, rely=1.0, anchor="sw")
        self.my_canvas.pack()

        self.setup()
        self.load_model(model_path)
        self.window.mainloop()

    def setup(self):
        self.my_canvas.bind("<Button-3>", self.clear_sketchbook)
        self.my_canvas.bind("<Button-2>", self.predict_number)
        self.my_canvas.bind("<B1-Motion>", self.draw_event)

    def draw_event(self, event):
        self.x = event.x
        self.y = event.y

        r = 30

        # Determine the coordinates of the area in which the circle will appear
        self.x1 = self.x - r
        self.y1 = self.y - r
        self.x2 = self.x + r
        self.y2 = self.y + r

        self.my_canvas.create_oval((self.x1, self.y1, self.x2, self.y2), fill="black")

    def clear_sketchbook(self, event):
        self.my_canvas.delete("all")
        self.number_label.config(text="PREDICTED: NONE")

    def load_model(self, model_path):
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict_number(self, event):
        canvas_postscript = self.my_canvas.postscript(colormode="color")
        image = Image.open(io.BytesIO(canvas_postscript.encode("utf-8")))

        # Changing the image size to 8x8 px - getting an image similar to the training data
        image = image.resize((8, 8))
        image = image.convert(mode="L")
        image = np.array(image)
        image = np.invert(image)
        # Reshape an image matrix into a form [1, number_of pixels]
        image = image.reshape([1, -1])
        # Converting an 8-bit image matrix to 4-bit
        image = np.round(image / 16.0)

        prediction = self.model.predict(image)
        self.number_label.config(text="PREDICTED:" + str(prediction))


if __name__ == "__main__":
    App()
