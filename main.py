from tkinter import *
from tkinter import messagebox, filedialog

from ambTEX import ambTEX


window = Tk()
window.title("Arma3 Mod Builder")
window.resizable(False, False)


#Listeners
def compute():

    inst1 = ambTEX(e_sourF.get(), e_outF.get(), e_suffix.get())
    temp = inst1.getFiles()
    populates(lb_fileList, temp, inst1.getSize())
    
    try:

        inst1.convert2()
        lb_logList.insert(END, "Conversion complete!")

    except:

        lb_logList.insert(END, "Error when converting images!")



def clear():

    e_sourF.delete(0, END)
    tx_Year.set("")

    e_outF.delete(0, END)
    tx_Rate.set("")

    lb_fileList.delete(0, END)
    lb_logList.delete(0, END)



def exit():

    if (messagebox.askokcancel(title = "Exit", message = "Do you want to end the program?")):
        
        window.destroy()



def setFol(btn):

    window.directory = filedialog.askdirectory()
                  
    if(btn.config('text')[-1] == "Open"):

        setTxt(e_sourF, window.directory)

    else:

        setTxt(e_outF, window.directory)



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



#Labels
l_sourF = Label(window, text = "Source Folder", width = 10)
l_sourF.grid(row = 0, column = 0, sticky = W)

l_outF = Label(window, text = "Output Folder", width = 10)
l_outF.grid(row = 1, column = 0, sticky = W)

l_suffix = Label(window, text = "File Suffix", width = 7)
l_suffix.grid(row = 2, column = 0, sticky = W)

l_log = Label(window, text = "Logs", width = 3)
l_log.grid(row = 15, column = 0, sticky = W)


#Entries
tx_Year = StringVar()
e_sourF = Entry(window, textvariable = tx_Year, width = 40)
e_sourF.grid(row = 0, column = 1, sticky = W)

tx_Rate = StringVar()
e_outF = Entry(window, textvariable = tx_Rate, width = 40)
e_outF.grid(row = 1, column = 1, sticky = W)

tx_Suffix = StringVar()
e_suffix = Entry(window, textvariable = tx_Suffix, width = 10)
e_suffix.grid(row = 2, column = 1, sticky = W)


#Listbox
lb_fileList = Listbox(window, height = 20, width = 70)
lb_fileList.grid(row = 4, column = 0, rowspan = 10, columnspan = 2 , sticky = W) # we want to span across multiple rows and columns

sb_fileList = Scrollbar(window)
sb_fileList.grid(row = 4, column = 2, rowspan = 10, sticky = W)

lb_fileList.configure(yscrollcommand = sb_fileList.set)
sb_fileList.configure(command = lb_fileList.yview)




lb_logList = Listbox(window, height = 5, width = 70)
lb_logList.grid(row = 20, column = 0, rowspan = 10, columnspan = 2 , sticky = W) # we want to span across multiple rows and columns

sb_logList = Scrollbar(window)
sb_logList.grid(row = 20, column = 2, rowspan = 10, sticky = W)

lb_logList.configure(yscrollcommand = sb_logList.set)
sb_logList.configure(command = lb_logList.yview)


#Buttons
b1 = Button(window, text = "Compute", width = 12, command = compute)
b1.grid(row = 6, column = 3)
b2 = Button(window, text = "Clear", width = 12, command = clear)
b2.grid(row = 7, column = 3)
b3 = Button(window, text = "Exit", width = 12, command = exit)
b3.grid(row = 8, column = 3)

b4 = Button(window, text = "Open", width = 5, command = lambda : setFol(b4))
b4.grid(row = 0, column = 2, sticky = W)

b5 = Button(window, text = "Open2", width = 5, command = lambda : setFol(b5))
b5.grid(row = 1, column = 2, sticky = W)


#Option Menu
variable = StringVar(window)
variable.set("one") # default value

w = OptionMenu(window, variable, "one", "two", "three")
w.grid(row = 1, column = 3)


window.mainloop()