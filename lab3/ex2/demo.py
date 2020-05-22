# -*- coding: utf-8 -*-

from tkinter import *

from text_editor import TextEditor
from text_editor_model import TextEditorModel

if __name__ == '__main__':
    model = TextEditorModel(
#         """U mome kraju, brodovi su ljudi
# Oni plaču, smiju se i vole
# U mome kraju, brodovi su svečanost
# I najdraže igračke nestašnih dječaka
# Brodovi
# Bez vas, tužne su luke sve
# Bez vas, puste su rive te
# Bez vas, galebi mru
#
# Dok Mjesec kosi noć
# Na pramcu stiha svog
# Ja palim sreće žar
# Za puteve vaše
#
# Brodovi
# Na vas čekaju ljubavi
# Na vas čekaju prozori
# Bez vas, gitare mru
#
# Dok zora pali dan
# Na jarbol stiha svog
# Ja dižem pjesmu tu
# Za povratke vaše
#
# Dok zora pali dan
# Na jarbol stiha svog
# Ja dižem pjesmu tu
# Za povratke vaše
#
# O, igračke drage
# Iz djetinjstva mog"""
#         "This is the longest line ever in the world here ever longest really "
#         "longest too long for ordinary people for ordinary world too too long for anything in reality for real cmon "
#         "too long really too too too long\n"
#         "This is the longest line ever in the world here ever longest really "
#         "longest too long for ordinary people for ordinary world too too long for anything in reality for real cmon "
#         "too long really too too too long\n"
#         "This is the longest line ever in the world here ever longest really "
#         "longest too long for ordinary people for ordinary world too too long for anything in reality for real cmon "
#         "too long really too too too long\n"
        "The first line.\n"
        "In between the two...\n"
    "The last line.")

    root = Tk()
    tedi = TextEditor(model)
    root.geometry("555x800+300+300")
    root.mainloop()

"""
"Vidimo da osnovni razred omogućava da grafički podsustav samostalno poziva naš kod za crtanje kad god se za to 
javi potreba, iako je oblikovan i izveden davno prije naše grafičke komponente. Koji oblikovni obrazac to omogućava?" 
--> TODO 

"Vidimo također da naša grafička komponenta preko osnovnog razreda može dobiti informacije o pritisnutim tipkama 
bez potrebe za čekanjem u radnoj petlji. Koji oblikovni obrazac to omogućava?"
--> Observer
"""
