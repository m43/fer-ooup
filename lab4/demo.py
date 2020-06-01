# -*- coding: utf-8 -*-

from tkinter import *

from geometry.line_segment import LineSegment
from geometry.oval import Oval
from gui import Painter

if __name__ == '__main__':
    objects = []

    objects.append(LineSegment())
    objects.append(Oval())

    root = Tk()
    root.title("ma paint")
    root.geometry("600x741+210+120")
    painter = Painter(objects)
    root.mainloop()
