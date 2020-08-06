import cv2
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *

width = 400
height = 400
center = height//2
white = (255, 255, 255)
green = (0,128,0)

def save():
    # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
    # filename = "my_drawing.png"
    # image1.save(filename)
    filename = "image.png"
    image1.save(filename)

def paint(event):
    # python_green = "#476042"
    x1, y1 = event.x, event.y
    if cv.old_coords:
        x2, y2 = cv.old_coords
        cv.create_line(x1, y1, x2, y2, fill="black",width=5)
        draw.line([x1, y1, x2, y2],fill="black",width=5)
    cv.old_coords = x1, y1
    
def reset_coords(event):
    cv.old_coords = None

root = Tk()

# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg='white')
cv.pack()
cv.old_coords = None

# PIL create an empty image and draw object to draw on
# memory only, not visible
image1 = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image1)

cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)
cv.bind("<ButtonRelease-1>", reset_coords)
root.bind("<Escape>", lambda e: root.destroy())

# do the PIL image/draw (in memory) drawings
# draw.line([0, center, width, center], green)

button=Button(text="save",command=save)
button.pack()
root.mainloop()
