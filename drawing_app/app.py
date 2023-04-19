from tkinter import *

window = Tk()
window.title('Sketchbook')
window.geometry('500x500')

# Crate Canvas widget
my_canvas = Canvas(window, width=8, height=8, bg='white')
# Pack Canvas to thinket objet, anchow - starting point (north-west, (0, 0)); fill and expand  - stretch canvas to the grids
my_canvas.pack(anchor='nw', fill='both', expand=1)

numb = list()


def initial_cordinates(event):
    global x_cord, y_cord
    x_cord, y_cord = event.x, event.y
    cords = x_cord, y_cord
    numb.append(cords)


def draw(event):
    global x_cord, y_cord

    my_canvas.create_line((x_cord, y_cord, event.x, event.y),
                          fill='black', width=8)
    x_cord, y_cord = event.x, event.y
    cords = x_cord, y_cord
    numb.append(cords)


def clear_sketchbook(event):
    my_canvas.delete('all')
    numb.clear()


# Interaction with user
my_canvas.bind("<Button-1>", initial_cordinates)
my_canvas.bind("<B1-Motion>", draw)
my_canvas.bind("<Button-3>", clear_sketchbook)


window.mainloop()
