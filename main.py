# coding=utf-8
__author__ = 'moons'
import Tkinter as tk
import tkMessageBox as mb
import socket
import fivemap
import moonsn_netlib

mp = fivemap.Mp()
myIP = socket.gethostname()
myPORT = 50005
mycolor = 'w'
COLOR_B = "#34495E"
COLOR_W = "#D4E6F1"
NOW_COLOR = "B"


main_width = 600
main_height = 510

root = tk.Tk()
root.title("五点")

# 新建Canvas,在上面画棋盘
w = tk.Canvas(root, width=main_width, height=main_height)

# base rectangle
w.create_rectangle(0,0, main_width, main_height, fill="#FDFEFE")

# function for draw grid
def draw_grid(width, color):
    global main_width, main_height, w
    for i in range(30, main_width, width):
        w.create_line(i, 0, i, main_height, fill=color)
    for i in range(30, main_height, width):
        w.create_line(0, i, main_width, i, fill=color)

# for debug
def draw_grid2(width, color):
    global main_width, main_height, w
    for i in range(15, main_width, width):
        w.create_line(i, 0, i, main_height, fill=color)
    for i in range(15, main_height, width):
        w.create_line(0, i, main_width, i, fill=color)


def toggle():
    global COLOR_W,COLOR_B, NOW_COLOR
    if NOW_COLOR == "B":
        NOW_COLOR = "W"
        return COLOR_W
    else:
        NOW_COLOR = "B"
        return COLOR_B

def draw_dot(x, y):
    global main_width, main_height, w, COLOR_B, COLOR_W, NOW_COLOR
    COLOR = toggle()
    w.create_oval(x-13, y-13, x+13, y+13, fill=COLOR)

def up_bound(x, y):
    global mp, NOW_COLOR
    newx = (x / 30 + 1)*30 if (x % 30 > 15) else (x / 30)*30
    newy = (y / 30 + 1)*30 if (y % 30 > 15) else (y / 30)*30
    print ("Mouse position fix: (%s, %s)" % (newx, newy))
    draw_dot(newx, newy)
    print ("Map position: (%s, %s)" % (newx/30, newy/30))
    mp.setPos(newy/30-1, newx/30 -1, NOW_COLOR)
    res = mp.check()
    if res != None:
        print "%s win !!!!!!!!!!!!!!!!" % NOW_COLOR
        win(NOW_COLOR)


def win(color):
    global w
    mb.showinfo("game end", "%s win the game!" % (color))


def doit(event):
    #print ("Mouse position: (%s, %s)" % (event.x, event.y))
    up_bound(event.x, event.y)
    return

w.bind('<Button>', doit)
draw_grid(30, '#AED6F1')
#draw_grid2(30, '#E5E8E8')
w.pack()

root.mainloop()