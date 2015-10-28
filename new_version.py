# coding=utf-8

import Tkinter as tk
import fivemap
import moonsn_netlib
import json

listen_PORT = 50000
sendto_PORT = 50000
sendto_IP = '192.168.1.149'
MY_COLOR = None
COLOR_B = "#34495E"
COLOR_W = "#D4E6F1"
NOW_COLOR = "B"

UNIT = 30
ROW = 20
COL = 30
MAIN_HEIGHT = UNIT * ROW
MAIN_WIDTH = UNIT * COL



class Application(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.mp = fivemap.Mp(ROW, COL)

        self.initUI()


    def initUI(self):
        self.parent.title("simple menu")
        menu_bar = tk.Menu(self.parent)
        self.parent.config(menu=menu_bar)

        fileMenu = tk.Menu(menu_bar)
        fileMenu.add_command(label="exit", command=self.onExit)
        menu_bar.add_cascade(label="file", menu=fileMenu)
        self.draw_rect()

    def onExit(self):
        self.quit()

    def draw_rect(self):
        self.canvas = tk.Canvas()
        self.canvas.create_rectangle(0, 0, MAIN_WIDTH, MAIN_HEIGHT, fill="#FDFEFE")
        for i in range(UNIT, MAIN_WIDTH, UNIT):
            self.canvas.create_line(i, 0, i, MAIN_HEIGHT, fill="#AED6F1")
        for i in range(UNIT, MAIN_HEIGHT, UNIT):
            self.canvas.create_line(0, i, MAIN_WIDTH, i, fill="#AED6F1")
        self.canvas.bind("<Button>", self.doit)
        self.canvas.pack(fill="both", expand=1)


    def up_bound(self, x, y):
        new_x = (x / 30 + 1)*30 if (x % 30 > 15) else (x / 30)*30
        new_y = (y / 30 + 1)*30 if (y % 30 > 15) else (y / 30)*30
        print "relative position: (%s, %s)" % (x, y)
        print "fixed position: (%s, %s)" % (new_x, new_y)
        return new_x, new_y

    def on_border(self, row, col):
        global ROW, COL
        return True if col == 0 or row == 0 or col == COL or ROW == row else False

    def doit(self, event):
        fixed_x, fixed_y = self.up_bound(event.x, event.y)
        row, col = fixed_y/30, fixed_x/30

        if self.on_border(row, col) :
            return

        if not self.mp.isEmpty(row-1, col-1):
            return

        self.draw_dot(fixed_x, fixed_y)

        print ("Map position: (%s, %s)" % (row-1, col-1))
        self.mp.setPos(row-1, col-1, NOW_COLOR)

        # send my step
        msg = [{'row': row, 'col': col}]
        j_msg = json.dumps(msg)
        cli.sendMsg(j_msg)

        res = self.mp.check()
        if res != None:
            print "%s win !!!!!!!!!!!!!!!!" % NOW_COLOR
            #draw_win(NOW_COLOR)


    def draw_dot(self, x, y):
        COLOR = self.toggle()
        self.canvas.create_oval(x-13, y-13, x+13, y+13, fill=COLOR)

    def toggle(self):
        global COLOR_W,COLOR_B, NOW_COLOR
        if NOW_COLOR == "B":
            NOW_COLOR = "W"
            return COLOR_W
        else:
            NOW_COLOR = "B"
            return COLOR_B

    @classmethod
    def draw_other(self, str):
        global mp,cli,NOW_COLOR
        str = json.loads(str)
        row = str[0]['row']
        col = str[0]['col']
        self.draw_dot(self,(col + 1)*30, (row + 1)*30)
        mp.setPos(row, col, NOW_COLOR)

        res = self.mp.check()
        if res != None:
            print "%s win !!!!!!!!!!!!!!!!" % NOW_COLOR
            #self.draw_win(NOW_COLOR)

app = None
# for network
ser = moonsn_netlib.Server(listen_PORT, app.draw_other)
ser.start()
cli = moonsn_netlib.Client(sendto_IP,sendto_PORT)
cli.start()

def main():
    global app
    root = tk.Tk()
    root.geometry("%sx%s+300+300" % (MAIN_WIDTH, MAIN_HEIGHT))
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()


