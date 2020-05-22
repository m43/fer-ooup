#!/usr/bin/env python3

from tkinter import *

class TextEditor(Frame):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.master.title("Lab 3 example")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar)

        submenu = Menu(file_menu)
        submenu.add_command(label="New feed")
        submenu.add_command(label="Bookmarks")
        submenu.add_command(label="Mail")
        file_menu.add_cascade(label='Import', menu=submenu, underline=0)

        file_menu.add_separator()

        file_menu.add_command(label="Exit", underline=0, command=self.on_exit)
        menubar.add_cascade(label="File", underline=0, menu=file_menu)

        self._canvas = Canvas(self, bg="white")

        self._canvas.create_line(15, 25, 200, 25)
        self._canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        self._canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

        self._canvas.create_rectangle(30, 10, 120, 80, outline="#fb0", fill="#fb0")
        self._canvas.create_rectangle(150, 10, 240, 80, outline="#f50", fill="#f50")
        self._canvas.create_rectangle(270, 10, 370, 80, outline="#05f", fill="#05f")

        self._canvas.create_oval(10, 10, 80, 80, outline="#f11", fill="#1f1", width=2)
        self._canvas.create_oval(110, 10, 210, 80, outline="#f11", fill="#1f1", width=2)
        self._canvas.create_rectangle(230, 10, 290, 60, outline="#f11", fill="#1f1", width=2)
        self._canvas.create_arc(30, 200, 90, 100, start=0, extent=210, outline="#f11", fill="#1f1", width=2)

        points = [150, 100, 200, 120, 240, 180, 210, 200, 150, 150, 100, 200]
        self._canvas.create_polygon(points, outline='#f11', fill='#1f1', width=2)

        self._canvas.create_rectangle(55, 15, 150, 75, fill="yellow")
        self._canvas.create_line(55, 15, 100, 15, fill="red", dash=(4, 4))
        self._canvas.create_line(0, 10, 300, 10, fill="#FF2211", width=3)
        self._canvas.create_line(50, 10, 50, 300, fill="#FF2211", width=3)

        self._canvas.create_text(55, 15, fill="darkblue", anchor=NW, font="Times 20 italic bold", text="Ja sam Frano")

        self._canvas.create_text(20, 30, anchor=W, font="Purisa", text="Most relationships seem so transitory")
        self._canvas.create_text(20, 60, anchor=W, font="Purisa", text="They're good but not the permanent one")
        self._canvas.create_text(20, 130, anchor=W, font="Purisa", text="Who doesn't long for someone to hold")
        self._canvas.create_text(20, 160, anchor=W, font="Purisa", text="Who knows how to love without being told")
        self._canvas.create_text(20, 190, anchor=W, font="Purisa", text="Somebody tell me why I'm on my own")
        self._canvas.create_text(20, 220, anchor=W, font="Purisa", text="If there's a soulmate for everyone")

        self._canvas.create_text(20, 250, width=380, anchor=NW, font="Purisa",
                                 text="Most relationships seem so transitory they're good but not the permanent one who doesn't long for someone to hold who knows how to love without being told Somebody tell me why I'm on my own If there's a soulmate for everyone")
        self._canvas.pack(fill=BOTH, expand=1)

    def on_exit(self):
        self.master.quit()


if __name__ == '__main__':
    root = Tk()
    ex = TextEditor()
    root.geometry("555x800+300+300")
    root.mainloop()
