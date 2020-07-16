import tkinter as tk

def draw(event):
    x, y = event.x, event.y
    if canvas.old_coords:
        x1, y1 = canvas.old_coords
        canvas.create_line(x, y, x1, y1)
    canvas.old_coords = x, y

def reset_coords(event):
    canvas.old_coords = None

root = tk.Tk()

canvas = tk.Canvas(root, width=500, height=400)
canvas.pack()
canvas.old_coords = None

#클릭시 선 그림
# tkinter 관련 마우스 이벤트에 관한 태그들 BIND 기능 --> https://bit.ly/3eD0XbH / https://076923.github.io/posts/Python-tkinter-23/
root.bind('<B1-Motion>', draw)

#클릭을 땠을 경우 다시 클릭했을 때 이전에 그렸던 선들과 연결되지 않게 만듬
root.bind('<ButtonRelease-1>', reset_coords)

root.mainloop()