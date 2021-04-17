#from tkinter import *
from tkinter import messagebox, filedialog, Listbox, Label, Entry, Button, OptionMenu, StringVar, Scrollbar, Tk, N, S, W, E, END
from tkinter import ttk, Menu, Toplevel, Text, DISABLED, HORIZONTAL
from ambTEX import ambTEX



window = Tk()
window.title("Arma3 Mod Builder")
window.resizable(False, False)



#Listeners
def compute():
    
    if(not isValid()):
        return
    
    pb_progbar['value'] = 0
    inst1 = ambTEX(e_sourF.get(), e_outF.get(), e_suffix.get(), lb_logList)
    window.update_idletasks()

    try:

        if(tx_Mode.get() == "DGE-OVL"):

            inst1.convert2()

        else:
            
            inst1.convert()

        pb_progbar['value'] = 100
        lb_logList.insert(END, "Conversion complete!")

    except:

        lb_logList.insert(END, "Error when converting images!")



def clear():

    e_sourF.delete(0, END)
    tx_sourF.set("")

    e_outF.delete(0, END)
    tx_outF.set("")

    lb_fileList.delete(0, END)
    lb_logList.delete(0, END)

    pb_progbar['value'] = 0
    pb_progbar.stop()
    


def exit():

    if (messagebox.askokcancel(title = "Exit", message = "Do you want to end the program?")):
        
        window.destroy()



def setFol(btn):

    window.directory = filedialog.askdirectory()
                  
    if(btn.config('text')[-1] == "Open"):
        
        setTxt(e_sourF, window.directory)
        inst2 = ambTEX(e_sourF.get(), e_outF.get(), e_suffix.get(), lb_logList)
        populates(lb_fileList, inst2.getFiles(), inst2.getSize())
        del inst2
        
    else:

        setTxt(e_outF, window.directory)
        


def infoBar():
    
    window2 = Toplevel(window)
    window2.geometry("500x600")
    window2.title("Help")
    window2.resizable(False, False)

    info = (
    """
    1. Program generates a PBR-looking diffuse map(_co) with 
       PBR-Spec-Gloss textures exported from Substance Painter. \n                                                         
    2. Program automatically detects all UV sets and process them
       one by one. \n
    3. All files must be named with proper suffix eg,: \n
       "XXXX_01_co.png"
       "XXXX_01_as.png"
       "XXXX_01_nohq.png"
       "XXXX_01_smdi.png" ...etc. \n
       "XXXX_02_co.png"
       "XXXX_02_as.png"
       "XXXX_02_nohq.png"
       "XXXX_02_smdi.png" ...etc. \n
    4. Naming Conventions:  ('_0x' being the UV set ID) \n
       Diffuse:             _0x_co
       Normal:              _0x_nohq
       Normal_OpenGL:       _0x_opgl
       Ambient Occlusion:   _0x_as
       Spec_Arma:           _0x_smdi
       Specular:            _0x_spec
       Height:              _0x_ht
       Glossiness:          _0x_gloss \n
    5. Blending Mode: \n
       DGE-OVL:
          _spec
                >DODGE
          _gloss
                >OVERLAY
          _co \n
       DO-NOR:
          _spec
                >DARKEN ONLY
          _co
                >NORMAL

    """)

    text = Text(window2, height = 600)
    text.insert(END, info)
    text.configure(state = DISABLED)
    text.pack()



def ctktBar():
    
    window3 = Toplevel(window)
    window3.geometry("500x100")
    window3.title("Contact")
    window3.resizable(False, False)

    info = (
    """
    1. Program is written in Python and if anyone is
       interested feel free to modify the source code
       and push it into a new branch then request a review. \n
    2. Contact me at:
       lzblmvm@gmail.com
    """)

    text2 = Text(window3, height = 100)
    text2.insert(END, info)
    text2.configure(state = DISABLED)
    text2.pack()



#Functions
def setTxt(e, v):

    e.delete(0, END)
    e.insert(0, v)



def populates(lb, dic, size):

    temp = list(dic.items())

    try:

        for k, v in temp:

            lb.insert(END, k)

            for i in v:

                info = "{Mes: >30}".format(Mes = i)
                lb.insert(END, info)

        lb_logList.insert(END, str(len(temp)) + " UV group(s) detected, " + str(size) + " files added.")

    except:

        lb_logList.insert(END, "Error when adding files!")



def isValid():

    if (e_sourF.get() == ""):
        lb_logList.insert(END, "Set I/O directories first!")
        return False

    if (e_outF.get() == ""):
        lb_logList.insert(END, "Set I/O directories first!")
        return False

    elif (e_sourF.get() == e_outF.get()):
        lb_logList.insert(END, "I/O directories must be different!")
        return False

    else:
        return True



#Menu
menubar = Menu(window)
filemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Help", menu = filemenu)
filemenu.add_command(label="Usage", command = infoBar)
filemenu.add_separator()
filemenu.add_command(label="Contact", command = ctktBar)



#Labels
l_sourF = Label(window, text = "Source Folder", width = 10)
l_sourF.grid(row = 0, column = 0, sticky = W)

l_outF = Label(window, text = "Output Folder", width = 10)
l_outF.grid(row = 1, column = 0, sticky = W)

l_suffix = Label(window, text = "File Suffix", width = 7)
l_suffix.grid(row = 2, column = 0, sticky = W)

l_log = Label(window, text = "Logs", width = 3)
l_log.grid(row = 15, column = 0, sticky = W)

l_mode = Label(window, text = "Mixing Mode", width = 10)
l_mode.grid(row = 3, column = 0, sticky = W)



#Entries
tx_sourF = StringVar()
e_sourF = Entry(window, textvariable = tx_sourF, width = 40)
e_sourF.grid(row = 0, column = 1, sticky = W)

tx_outF = StringVar()
e_outF = Entry(window, textvariable = tx_outF, width = 40)
e_outF.grid(row = 1, column = 1, sticky = W)

tx_Suffix = StringVar(window, "_0x")
e_suffix = Entry(window, textvariable = tx_Suffix, state = DISABLED, width = 10)
e_suffix.grid(row = 2, column = 1, sticky = W)



#Listbox
lb_fileList = Listbox(window, height = 20, width = 70)
lb_fileList.grid(row = 4, column = 0, rowspan = 10, columnspan = 2 , sticky = W)

sb_fileList = Scrollbar(window)
sb_fileList.grid(row = 4, column = 2, rowspan = 10, sticky = W)

lb_fileList.configure(yscrollcommand = sb_fileList.set)
sb_fileList.configure(command = lb_fileList.yview)


lb_logList = Listbox(window, height = 5, width = 70)
lb_logList.grid(row = 20, column = 0, rowspan = 10, columnspan = 2 , sticky = W)

sb_logList = Scrollbar(window)
sb_logList.grid(row = 20, column = 2, rowspan = 10, sticky = W)

lb_logList.configure(yscrollcommand = sb_logList.set)
sb_logList.configure(command = lb_logList.yview)



#ProgressBar
pb_progbar = ttk.Progressbar(window, orient = HORIZONTAL, length = 425, mode = 'determinate')
pb_progbar.grid(row = 30, column = 0, rowspan = 10, columnspan = 2 , sticky = W)



#Buttons
b1 = Button(window, text = "Convert", width = 12, command = compute)
b1.grid(row = 6, column = 3)
b2 = Button(window, text = "Clear", width = 12, command = clear)
b2.grid(row = 7, column = 3)
b3 = Button(window, text = "Exit", width = 12, command = exit)
b3.grid(row = 8, column = 3)

b4 = Button(window, text = "Open", width = 5, command = lambda : setFol(b4))
b4.grid(row = 0, column = 2, sticky = W)

b5 = Button(window, text = "Set", width = 5, command = lambda : setFol(b5))
b5.grid(row = 1, column = 2, sticky = W)



#Option Menu
tx_Mode = StringVar()
tx_Mode.set("DGE-OVL") 

om_mixM = OptionMenu(window, tx_Mode, "DGE-OVL", "DO-Nor")
om_mixM.grid(row = 3, column = 1, sticky = W)



window.config(menu = menubar)
window.mainloop()