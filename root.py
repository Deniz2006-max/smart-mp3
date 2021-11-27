from tkinter import *

def skillUsed():
    if chkUsedVar.get() == 1:
        opt01.configure(bg="#000fff000")
        opt01.configure(highlightbackground="#000fff000")
        opt01.configure(activebackground="#000fff000")
        opt01.configure(highlightcolor="#000fff000")
        opt01["menu"].configure(bg="#000fff000")
    else:
        opt01.configure(bg=orgOptbg)
        opt01.configure(highlightbackground=orgOpthighlightbackground)
        opt01.configure(activebackground=orgOptactivebackground)
        opt01.configure(highlightcolor=orgOpthighlightcolor)
        opt01["menu"].configure(bg=orgOptmenu)

root = Tk()
optionList = ('parrot','silly','walk')
varopt01 = StringVar()
varopt01.set(optionList[0])
chkUsedVar = IntVar()

opt01 = OptionMenu(root, varopt01, *optionList)
opt01.grid(row=0, column=0)

orgOptbg = opt01.cget("bg")
orgOpthighlightbackground = opt01.cget("highlightbackground")
orgOptactivebackground = opt01.cget("activebackground")
orgOpthighlightcolor = opt01.cget("highlightcolor")
orgOptmenu = opt01["menu"].cget("bg")

chk = Checkbutton(root, text='Used', variable=chkUsedVar, command=skillUsed)
chk.grid(row=0, column=1)
root.mainloop()