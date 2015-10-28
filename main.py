# coding=utf-8
__author__ = 'moons'
import Tkinter as tk
import tkMessageBox as mb
import socket
import json
import fivemap
import moonsn_netlib

listen_PORT = 50000
sendto_PORT = 50000
sendto_IP = '192.168.1.121'
MY_COLOR = None
COLOR_B = "#34495E"
COLOR_W = "#D4E6F1"
NOW_COLOR = "B"

COL = 30
ROW = 20
main_width  =  COL * 30
main_height = ROW * 30

mp = fivemap.Mp(ROW, COL)

root = tk.Tk()
root.title("五点")




# add menus
def add_menus():
    print "fuck!"
    menu = tk.Menu(root)
    root.config(menu=menu)
    print "fuck!"
    menu.add_cascade(label="设置对手ip", command=hello)
    menu.add_cascade(label="new", command=new_game)

def hello():
    global et
    master = tk.Tk()
    tk.Label(master, text="对手IP").grid(row=0)
    et = tk.Entry(master)
    et.grid(row=0, column=1)

    tk.Button(master, text='Set', command=lambda:set_ip(et)).grid(row=0, column=2, pady=4, padx=4)

def set_ip(et):
    global sendto_IP
    sendto_IP = et.get()
    print "set other ip is :", sendto_IP




def add_Canvas():
    # 新建Canvas,在上面画棋盘
    global w
    w = tk.Canvas(root, width=main_width, height=main_height)

    # base rectangle
    w.create_rectangle(0,0, main_width, main_height, fill="#FDFEFE")
    w.bind('<Button>', doit)
    w.pack(fill="both")
    draw_grid(30, '#AED6F1')

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
    global mp, NOW_COLOR, cli, mp
    newx = (x / 30 + 1)*30 if (x % 30 > 15) else (x / 30)*30
    newy = (y / 30 + 1)*30 if (y % 30 > 15) else (y / 30)*30
    #print ("Mouse position fix: (%s, %s)" % (newx, newy))
    #draw_dot(newx, newy)
    #print ("Map position: (%s, %s)" % (newx/30, newy/30))
    return newx, newy




def onBorder(col, row):
    global ROW, COL
    print row, col
    return True if col == 0 or row == 0 or col == COL or ROW == row else False

def doit(event):
    #print ("Mouse position: (%s, %s)" % (event.x, event.y))
    global mp
    col, row = up_bound(event.x, event.y)

    if onBorder(col/30, row/30) :
        return

    if not mp.isEmpty(row/30-1, col/30-1):
        return

    draw_dot(col, row)

    row, col = row / 30 - 1, col / 30 - 1

    print ("Map position: (%s, %s)" % (row, col))
    mp.setPos(row, col, NOW_COLOR)

    # send my step
    msg = [{'row': row, 'col': col}]
    jmsg = json.dumps(msg)
    cli.sendMsg(jmsg)

    res = mp.check()
    if res != None:
        print "%s win !!!!!!!!!!!!!!!!" % NOW_COLOR
        draw_win(NOW_COLOR)



def draw_other(str):
    global mp,cli,NOW_COLOR
    str = json.loads(str)
    row = str[0]['row']
    col = str[0]['col']
    draw_dot((col + 1)*30, (row + 1)*30)
    mp.setPos(row, col, NOW_COLOR)

    res = mp.check()
    if res != None:
        print "%s win !!!!!!!!!!!!!!!!" % NOW_COLOR
        draw_win(NOW_COLOR)

def draw_win(color):
    master = tk.Tk()
    msg = "%s win the game!" % color
    tk.Label(master, text=msg).grid(row=0)
    tk.Button(master, text='OK', command=master.destroy).grid(row=1, pady=4, padx=4)



#draw_grid(30, '#AED6F1')
#draw_grid2(30, '#E5E8E8')

# for network
ser = moonsn_netlib.Server(listen_PORT, draw_other)
ser.start()
cli = moonsn_netlib.Client(sendto_IP,sendto_PORT)
cli.start()

def new_game():
    global mp,w
    mp.reset()
    print "reset game!"
    #mp.print_map()
    add_menus()
    w.destroy()
    add_Canvas()



#root.mainloop()
def main():
    add_menus()


    add_Canvas()
    root.mainloop()


if __name__ == '__main__':
    main()