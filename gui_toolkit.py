"""first of all: I HATE being "forced" to code GUI and i am not good at it or very familiar whit it either, but since my
program is for broader use in the FS-Community... there is not much i can do, as get along with it. And while all of my logic
works quite good, i still have some issues whit the gui workflow, which i decided to ignore for now and be ok whit the workarounds i came up with
while I finish my first release of this "program". But anybody who is familiar whit, "realtime-update" of the windows,
your very welcome to help me out ;) """

import queue
import tkinter
from pprint import pprint
from tkinter import scrolledtext

import my_comandos
import randomone
from my_comandos import runProgram
from randomone import SomethingDing


class TkUpdateQueue(queue.Queue):
    """one try to solve the problem of not immediately showing info in the text-widget...
    did not work at all :'''D
    of course the moment something got puted into the queue, is far ahead of the actual moment the widget, 
    gets the info and inserted it....
    but at least it could have worked whit one item spare...., 
    but as i sayed.... it did not at all :''''( xD actually it blocked"""
    def __init__(self):
        super().__init__()
        self.windows = None

    def register(self, *windows):
        self.windows = windows

    def put(self, item, block=True, timeout=None):
        [w.counterUpdate() for w in self.windows]
        super().put(item=item)

class LoggingWindow:

    def __init__(self, input_queue=randomone.DevQueue()):
        self.tk = tkinter.Toplevel()
        self.input_queue = input_queue
        self.logging_frame = tkinter.Frame(self.tk)
        self.label = tkinter.Label(self.logging_frame, text="Status:")
        self.label.pack(side=tkinter.TOP)
        self.text = tkinter.scrolledtext.ScrolledText(self.logging_frame)
        self.text.insert(tkinter.END, "Gestartet\nVerbindungen zu Foodsharing und Google werden aufgebaut.......\n")
        self.text.pack(side=tkinter.TOP)
        self.delete_psw_button = tkinter.Button(self.logging_frame, text="Passwort nicht mehr merken",
                                                command=my_comandos.deletePasswordAndEmail)
        self.logging_frame.pack(side=tkinter.LEFT)
        self.tk.after(80, self.job)
        self.delete_psw_button.pack(side=tkinter.BOTTOM)

    def update(self):
        self.tk.update()

    def counterUpdate(self):     #wont work in connection whit other threads an queue
        self.text.after(30, self.text.update)
        self.text.after(30, self.text.update_idletasks())

    def insert(self, text): #how can i make color color ????!!!
        self.text.insert(tkinter.END, text)
        self.text.insert(tkinter.END, "\n")
        self.text.pack_forget()   # workaround or right?!?
        self.text.pack()

    def job(self):
        self.tk.after(20, lambda : self.job())
        try:
            text = self.input_queue.get(block=False)
            print("versucht")
            self.insert(text)
            self.tk.update_idletasks()
            self.tk.update()
        except:
            pass

    def result(self, result_dict): #not totally shure if this is the right place to implement, 
                                    #but in a small code like here it is ok i think
        self.conflict_frame = tkinter.Frame(self.tk)
        self.conflict_frame.pack(side=tkinter.LEFT)
        self.conflict_label = tkinter.Label(self.conflict_frame, text="Konflikte:")
        self.conflict_label.pack(side=tkinter.TOP)
        self.conflict_text = tkinter.scrolledtext.ScrolledText(self.conflict_frame)

        for conflict_kind in result_dict:
            if conflict_kind in ("changed_appointment???", "alarm" , "warning", "forgotten something again, IDIOT"):
                set_here, list_here = result_dict[conflict_kind]
                # if first:
                #     first=False
                self.conflict_text.insert(tkinter.END, conflict_kind)

                for fs_date, google_date in list_here:
                    report = f"""
Foodsharing Termin:{' '*20}Googletermin:
{fs_date.start}{' '*20}{google_date.start}
{fs_date.summary:29s}{' '*10}{google_date.summary:29s}
"""
                    self.conflict_text.insert(tkinter.END, report)
        self.conflict_text.pack(side=tkinter.TOP)
        self.tk.update_idletasks()


class LEntry(tkinter.Frame):
    def __init__(self, master=None, one_two:list=False):
        super().__init__(master=master)

        self.lbframe = tkinter.Frame(self)
        self.eml_lable = tkinter.Label(master=self.lbframe, text="E-Mail:    ",anchor=tkinter.W)
        self.pwsd_lable = tkinter.Label(master=self.lbframe, text="Passwort:", anchor=tkinter.W)
        self.pwsd_lable.pack(side=tkinter.BOTTOM, padx=5, ipadx=3)
        self.eml_lable.pack(side=tkinter.BOTTOM, padx=5, ipadx=3)
        self.lbframe.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)

        self.entry_frame = tkinter.Frame(self)
        self.eml_ent = tkinter.Entry(master=self.entry_frame, width=40)
        self.pwsd_ent = tkinter.Entry(master=self.entry_frame, show="*", width=40)
        if one_two:
            self.eml_ent.insert(0, one_two[0])
            self.pwsd_ent.insert(0, one_two[1])
        self.entry_frame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)
        self.pwsd_ent.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.X)
        self.eml_ent.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.X)

        #Todo Internationalisation either picture Buttons german/englisch or listbox if there is french, italy, etc.

        self.ok_button = tkinter.Button(master=self, text="OK", command=self.okCallBack)
        self.ok_button.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)

    def okCallBack(self):
        # try:
        self.master.startFSProgramm(self.eml_ent.get(), self.pwsd_ent.get())
        # except:
        #     tkinter.messagebox.showerror(title="LogIn Error", message="Fehlerhafte Anmeldedaten")


class LockingInFrame(tkinter.Frame):
    def __init__(self, master=None, one_two:list=False):
        super().__init__(master=master)
        pprint(self.__dict__)

        self.remember_var = tkinter.BooleanVar()
        self.remember_checkb = tkinter.Checkbutton(master=self, text="Passwort merken", anchor=tkinter.W,
                                                   variable=self.remember_var, onvalue=True, offvalue=False)
        self.remember_checkb.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.X)

        self.l_entry = LEntry(master=self, one_two=one_two)
        self.l_entry.pack(side=tkinter.BOTTOM, expand=True, anchor=tkinter.W)

        self.what_is = tkinter.Label(master=self, text="Foodsharing-Login:", justify=tkinter.LEFT, anchor=tkinter.W)
        self.what_is.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.X, padx=4)

    def startFSProgramm(self, eml, pwsd):
        self.master.startFSProgramm(eml, pwsd, self.remember_var.get())



class Startframe(tkinter.Frame):
    def __init__(self, master=None, first=True, one_two:list=False):
        self._tk = master if master else tkinter.Tk()
        super().__init__(master=master)

        self.first = first
        self.master.wm_title("Foodsharing Calendar v0.1")
        #todo programm icon
        self.text = self.text()  #noticed after my uplade here wont cange it now
        if not master:
            self.pack(expand=True, fill="both")
        entry = LockingInFrame(master=self, one_two=one_two)
        entry.pack(side=tkinter.LEFT)

    def text(self):
        text = scrolledtext.ScrolledText(self, wrap=tkinter.WORD)
        loader = SomethingDing("filas1.tsm", something="lauterzeug")
        text.insert((0.0 ), '\n'.join(loader.load()))
        text.pack(side=tkinter.TOP, expand=True, fill="both")
        text.tag_add("center-all", 0.0, tkinter.END)
        text.tag_configure("center-all", justify=tkinter.CENTER)
        return text

    def startFSProgramm(self, eml, pwsd, remember):
        runProgram(eml, pwsd, remember, main_window=self, first=self.first)

