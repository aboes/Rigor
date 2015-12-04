import tkinter as tk
from tkinter import Label, Button, Radiobutton, Checkbutton, OptionMenu
from tkinter import ttk

from os import walk
import json
from time import time
from random import shuffle

LARGE_FONT = ("Verdana", 14)
ANSWER_FONT = ("Verdana", 20, "bold")
SMALL_FONT = ("Verdana", 8)

GROUP_SIZE = 4  # Für Patience-Mode

def readfile(filename):
    
    file = filename
    f = open(file, encoding="utf-8")
    r = f.read()
    f.close()
    return r

def savefile(filename, data):
    f = open(filename, "w", encoding="utf-8")
    r = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
    f.write(r)
    f.close()

class AlexRigor(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="varia/rigoricon.ico")
        tk.Tk.title(self, "Alex' Rigor")

        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in [StartPage, OptionsPage, QuizPage]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
    

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        label = ttk.Label(self, text="StartPage", font=LARGE_FONT)
        label.pack(padx=10, pady=20)
        
        korp_file = []
        for (dirpath, dirnames, filenames) in walk("data"):
            korp_file.extend(filenames)
            break
        korp_name = []
        for name in korp_file:
            p = name.find(".")
            korp_name.append(name[:p])
            
        opmenugroup = tk.Frame(self)
        THEMEN = korp_name
        opt_theme = tk.StringVar()
        opmenu_theme = ttk.OptionMenu(opmenugroup, opt_theme, "Thema wählen", *THEMEN)
        opmenu_theme.pack(side=tk.LEFT)
        
        opt_subset = tk.StringVar()
        
        def update_subset(self, *args):
            opmenu_subset["menu"].delete(0, "end")
            
            fname = "data/" + opt_theme.get() + ".korp"
            rawread = readfile(fname)
            korpus = json.loads(rawread)
            new_subset = []
            for i in korpus:
                new_subset.append(i["subset"]["name"])
            
            for choice in new_subset:
                opmenu_subset["menu"].add_cascade(label=choice,
                                                    command=tk._setit(opt_subset, choice))
        
        opt_subset.set("Subset wählen")
        opmenu_subset = ttk.OptionMenu(opmenugroup, opt_subset)
        opmenu_subset.pack(side=tk.LEFT)
        opmenugroup.pack(side=tk.TOP, padx=10, pady=5)
        
        def enable_start(self, *args):
            but_start.configure(state=tk.NORMAL)
        
        opt_theme.trace("w", update_subset)
        opt_subset.trace("w", enable_start)
        
        radiogroup = tk.Frame(self)
        MODES = [("Anschauen", 1), ("Patience", 2), ("Gruppiert", 3), ("Alle", 4)]
        self.opt_modes = tk.StringVar()
        self.opt_modes.set("1")
        for text, mode in MODES:
            radio_modes = ttk.Radiobutton(radiogroup, text=text, variable=self.opt_modes, value=mode)
            radio_modes.pack(side=tk.LEFT)
        radiogroup.pack(side=tk.TOP, padx=10, pady=5)
        
        buttongroup = tk.Frame(self)
        but_option = ttk.Button(buttongroup, text="Optionen",
                            command=lambda: controller.show_frame(OptionsPage))
        but_option.pack(side=tk.LEFT)
        
        but_start = ttk.Button(buttongroup, text="Start", state=tk.DISABLED,
                            command=lambda: self.goto_quizpage(opt_theme, opt_subset))
        but_start.pack(side=tk.LEFT)
        buttongroup.pack(side=tk.TOP, padx=10, pady=20)
        
    def goto_quizpage(self, opt_theme, opt_subset):
        self.controller.show_frame(QuizPage)
        self.controller.frames[QuizPage].clear_entry_answ()
        t = opt_theme.get()
        s = opt_subset.get()
        self.controller.frames[QuizPage].submit_topic(t, s)
        

class OptionsPage(tk.Frame):
    
    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        rawread = readfile("varia/options.opt")
        self.options = json.loads(rawread)
        self.modus = ""
        
        label = ttk.Label(self, text="Optionen", font=LARGE_FONT)
        label.pack(padx=10, pady=20)
        
        self.cvar_capit = tk.IntVar()
        self.cvar_help1 = tk.IntVar()
        self.cvar_help2 = tk.IntVar()
        self.cvar_alter = tk.IntVar()
        self.cvar_time = tk.IntVar()
        
        self.cvar_capit.set(self.options[0])
        self.cvar_help1.set(self.options[1])
        self.cvar_help2.set(self.options[2])
        self.cvar_alter.set(self.options[3])
        self.cvar_time.set(self.options[4])
        
        check_capit = ttk.Checkbutton(self, text="Grossschreibung ignorieren", variable=self.cvar_capit, width=35)
        check_capit.pack()
        check_help1 = ttk.Checkbutton(self, text="1. Hilfe: Ersten Buchstaben anzeigen", variable=self.cvar_help1, width=35)
        check_help1.pack()
        check_help2 = ttk.Checkbutton(self, text="2. Hilfe: Anzahl Buchstaben anzeigen", variable=self.cvar_help2, width=35)
        check_help2.pack()
        check_alter = ttk.Checkbutton(self, text="Alternative Schreibungen zulassen", variable=self.cvar_alter, width=35)
        check_alter.pack()
        check_time = ttk.Checkbutton(self, text="Zeitbeschränkung (5 Sekunden)", variable=self.cvar_time, width=35, state=tk.DISABLED)
        check_time.pack()
        
        but_back = ttk.Button(self, text="zurück",
                            command=self.save_and_back)
        but_back.pack(padx=10, pady=20)
        
    def save_and_back(self):
        tmp1 = self.cvar_capit.get()
        tmp2 = self.cvar_help1.get()
        tmp3 = self.cvar_help2.get()
        tmp4 = self.cvar_alter.get()
        tmp5 = self.cvar_time.get()
        self.options = [tmp1, tmp2, tmp3, tmp4, tmp5]
        savefile("varia/options.opt", self.options)
        self.controller.show_frame(StartPage)
        
class QuizPage(tk.Frame):
    
    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        self.options = []
        
        self.topic = ""
        self.subset = ""
        
        self.korpus = []
        self.patience = []
        
        self.qrounds = 0
        self.k_len = 0
        self.grps = 0
        self.qnum = 0
        self.state = ""
        self.symbol_count = 0
        
        self.titel = tk.StringVar()
        label = ttk.Label(self, textvariable=self.titel, font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        self.question = tk.StringVar()
        label_disp = ttk.Label(self, textvariable=self.question, font=LARGE_FONT)
        label_disp.pack()
        
        self.bemerkung = tk.StringVar()
        label_bmrk = ttk.Label(self, textvariable=self.bemerkung, font=SMALL_FONT)
        label_bmrk.pack()
        
        self.useranswer = tk.StringVar()
        self.entry_answ = ttk.Entry(self, textvariable=self.useranswer, font=ANSWER_FONT, justify=tk.CENTER)
        self.entry_answ.pack(fill=tk.X)
        
        self.pindicate = tk.StringVar()
        self.lab_pindi = ttk.Label(self, textvariable=self.pindicate, foreground="red", font=SMALL_FONT)
        self.lab_pindi.pack()
        
        self.response = tk.StringVar()
        label_resp = ttk.Label(self, textvariable=self.response, font=LARGE_FONT)
        label_resp.pack()
        
        frame_button = tk.Frame(self)
        frame_button.pack(padx=10, pady=10)
        self.but_help = ttk.Button(frame_button, text="Hilfe", command=self.givehelp)
        self.but_help.pack(side=tk.LEFT)
        
        self.but_enter = ttk.Button(frame_button, text="Enter", command=self.checkanswer)
        self.but_enter.pack(side=tk.LEFT, ipadx=20)
        self.but_next = ttk.Button(frame_button, text="Weiter", command=self.nextquestion)
        self.but_next.pack(side=tk.LEFT)
        
        self.indicator = tk.Label(self, bg="grey94", height=30)
        self.indicator.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.entry_answ.bind("<Return>", self.checkkey)
        self.but_enter.bind("<Return>", self.checkkey)
    
    def help2(self, fL):
        h_len = len(self.korpus[self.qnum]["feld_2"])
        lösung = self.korpus[self.qnum]["feld_2"]
        lösung = lösung.split()
        ldot = []
        for i in lösung:
            i = "*" * len(i)
            ldot.append(i)
        dots = " ".join(ldot)
        dots = fL + dots[1:]
        
        self.useranswer.set(dots)
        if fL == "":
            self.entry_answ.icursor(0)
        else:
            self.entry_answ.select_range(1, h_len)
    
    def givehelp(self):
        
        if self.options[1] == 1:
            firstLetter = self.korpus[self.qnum]["feld_2"][0]
            
            if self.korpus[self.qnum]["help"] == 0:
                self.useranswer.set(firstLetter)
                self.entry_answ.icursor(1)
        else:
            firstLetter = ""
            
        if self.options[2] == 1:
            if self.options[1] == 1 and self.korpus[self.qnum]["help"] > 0:
                self.help2(firstLetter)
            elif self.options[1] == 0 and self.korpus[self.qnum]["help"] == 0:
                self.help2(firstLetter)
                
        self.korpus[self.qnum]["help"] += 1
        self.entry_answ.focus_set()

    def check(self, uinput, solution, alternative):
        if self.options[0] == 1:
            uinput = uinput.lower()
            solution = solution.lower()
            alternative = [x.lower() for x in alternative]

        if self.options[3] == 1:
            answ1 = uinput == solution 
            answ2 = uinput in alternative  # alternative ist eine Liste. Prüfung: Ist Antwort in Liste vorhanden?
            answ = answ1 or answ2
        else:
            answ = uinput == solution
        
        return answ
            
    def checkanswer(self):
        self.state = "next"
        self.but_enter.config(state=tk.DISABLED)
        self.but_next.config(state=tk.NORMAL)
        ua = self.useranswer.get()
        ka = self.korpus[self.qnum]["feld_2"]
        al = self.korpus[self.qnum]["alt_2"]
        if al[0] != "": print(al)
        
        answ = self.check(ua, ka, al)
        if answ:
            self.response.set(self.korpus[self.qnum]["feld_2"] + " ist richtig!")
            self.indicator.configure(bg="green")
            self.korpus[self.qnum]["level"] += 1
            self.korpus[self.qnum]["verlauf"].append( [time(), 1] )
        else:
            if self.modus == "2":
                # self.useranswer.set(self.korpus[self.qnum]["feld_2"])
                self.entry_answ.config(state=tk.DISABLED)
                self.response.set("so wärs richtig: " + self.korpus[self.qnum]["feld_2"])
            else:
                self.response.set(ua + " ist falsch :-(")
            
            self.indicator.configure(bg="red")
            if self.korpus[self.qnum]["level"] > 0:
                self.korpus[self.qnum]["level"] -= 1
                
            self.korpus[self.qnum]["verlauf"].append( [time(), 0] )
            if self.modus == "2":
                self.symbol_count += 1
                symbol = "●" * self.symbol_count
                self.pindicate.set(symbol)
                
    def nextquestion(self):
        switch = self.modus
        if switch == "1":
            # Anschauen
            self.anschauenMode()
        elif switch == "2":
            # Patience
            self.entry_answ.config(state=tk.NORMAL)
            self.patienceMode()
        elif switch == "3":
            # Gruppiert
            # self.gruppiertMode()
            pass
        elif switch == "4":
            # Alle
            # self.alleMode()
            pass
            
    def anschauenMode(self):
        if self.state == "next":
            self.useranswer.set(self.korpus[self.qnum]["feld_2"])
            self.state = "enter"
            if self.qnum < self.k_len - 1:
                self.qnum += 1
            else:
                self.qrounds += 1
                self.qnum = 0
        else:
            if self.qrounds > 1:
                self.qrounds = 0
                self.controller.show_frame(StartPage)
            self.state = "next"
            self.useranswer.set("")
            self.question.set(self.korpus[self.qnum]["feld_1"])
            self.bemerkung.set(self.korpus[self.qnum]["bemerkung"])
        
    def patienceMode(self):        
        self.state = "enter"
        self.but_enter.config(state=tk.NORMAL)
        self.but_next.config(state=tk.DISABLED)
        self.useranswer.set("")
        self.response.set("")
        self.indicator.configure(bg="grey94")
        
        if self.qnum < len(self.korpus) - 1:                #  Prüfung: Subliste schon durch?
            self.qnum += 1
        else:                                               #  Wenn Subliste komplett durch
            self.patience[self.qrounds] = self.korpus
            self.qnum = 0
            richtige = 0
            for item in self.korpus:                        #  Anzahl Richtige der Subliste zählen
                if item["verlauf"][-1][1] > 0:
                    richtige += 1
                    
            if richtige == len(self.korpus):                #  In Subliste alle richtig:  Weiter
                self.qrounds += 1
                if self.qrounds == self.grps:               #  Prüfung: Alle Sublisten schon durch?
                    self.qrounds = 0
                    self.symbol_count = 0
                    self.pindicate.set("")
                    self.save_patience()
                    self.controller.show_frame(StartPage)
                else:                                       #  Wenn noch nicht alle Sublisten durch                    
                    self.korpus = self.patience[self.qrounds]
                    self.symbol_count = 0
                    self.pindicate.set("")
            
            if richtige == 0:                               #  In Subliste alle falsch:  Abbruch
                self.qrounds = 0
                self.symbol_count = 0
                self.pindicate.set("")
                self.save_patience()
                self.controller.show_frame(StartPage)
            
        # self.korpus = sorted(self.korpus, key=lambda k: k["level"])
        self.question.set(self.korpus[self.qnum]["feld_1"])
        self.bemerkung.set(self.korpus[self.qnum]["bemerkung"])
        self.entry_answ.focus_set()
        
    def save_korpus(self):
        fname = "data/" + self.topic + ".korp"
        rawread = readfile(fname)
        korpus = json.loads(rawread)
        for i in korpus:
            if i["subset"]["name"] == self.subset:
                i["subset"]["data"] = self.korpus
        savefile(fname, korpus)        

    def save_patience(self):
        self.korpus = [item for sublist in self.patience for item in sublist]  # Listcomprehension um self.patience zu flatten
        self.save_korpus()
        
    def checkkey(self, event):
        if self.state == "next":
            self.nextquestion()
        else:
            self.checkanswer()
        
    def start_quiz(self):
        if self.modus == "1":
            self.state = "next"
            self.but_next.configure(state=tk.NORMAL)
            self.but_enter.configure(state=tk.DISABLED)
            self.entry_answ.config(state=tk.DISABLED)
            self.but_next.focus_set()
            
            self.question.set(self.korpus[0]["feld_1"])
            
        elif self.modus == "2":
            self.state = "enter"
            self.but_next.configure(state=tk.DISABLED)
            self.but_enter.configure(state=tk.NORMAL)
            self.entry_answ.config(state=tk.NORMAL)
            self.entry_answ.focus_set()
            
            self.grps = self.k_len // GROUP_SIZE
            self.patience = [self.korpus[i::self.grps] for i in range(self.grps)]
            shuffle(self.patience)
            
            self.korpus = self.patience[0]
            self.question.set(self.korpus[0]["feld_1"])
            self.bemerkung.set(self.korpus[0]["bemerkung"])
        else:
            txt = "Modus noch nicht implementiert!"
            self.useranswer.set(txt)
            self.question.set(txt)
            self.but_help.configure(state=tk.DISABLED)
            self.but_next.configure(state=tk.DISABLED)
            self.but_enter.configure(state=tk.DISABLED)
            self.entry_answ.config(state=tk.DISABLED)        
        
        if self.options[1] == 0:
            if self.options[2] == 0:
                self.but_help.config(state=tk.DISABLED)
    
    def clear_entry_answ(self):
        self.useranswer.set("")        
        self.entry_answ.focus_set()
        
    def submit_topic(self, topic, subset):
        self.topic = topic
        self.subset = subset
        rawread = readfile("data/" + topic + ".korp")
        kall = json.loads(rawread)
        for i in kall:
            if i["subset"]["name"] == subset:
                self.korpus = i["subset"]["data"]
        self.k_len = len(self.korpus)
        self.options = self.controller.frames[OptionsPage].options
        self.modus = self.controller.frames[StartPage].opt_modes.get()
        self.titel.set(self.topic + ": " + self.subset)
        self.start_quiz()        

        
app = AlexRigor()
app.geometry("600x250+300+300")
app.mainloop()