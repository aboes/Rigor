"""Module Patience"""

import rigormodules.globals as GL

class Patience(GL.Frame):
    """GUI-Elemente und Logik für den Modus Patience"""
    def __init__(self, parent, controller):
        GL.Frame.__init__(self, parent)
        self.controller = controller

        self.topic = ""
        self.subtopic = ""
        self.korpus = []
        self.korpus_len = 0
        self.grps = 0
        self.patience = []
        self.pgrp_len = 0
        self.pgroup = 0
        self.pgnum = 0
        self.options = []
        self.richtige = 0
        self.falsche = 0
        self.snum = 0
        self.hnum = 0

        grp_titel = GL.Frame(self)
        lab_modus = GL.Label(grp_titel, text="Modus: Patience",
                             foreground=GL.COL_B1, font=GL.MEDIUM_FONT)
        lab_modus.pack(side=GL.LEFT)

        self.qcounter = GL.StringVar()
        lab_counter = GL.Label(grp_titel, textvariable=self.qcounter,
                               foreground=GL.COL_B1, font=GL.MEDIUM_FONT)
        lab_counter.pack(side=GL.RIGHT)
        grp_titel.pack(fill=GL.BOTH, padx=10)

        self.kategorie = GL.StringVar()
        lab_titel = GL.Label(self, textvariable=self.kategorie,
                             foreground=GL.COL_B1, font=GL.MEDIUM_FONT_2)
        lab_titel.pack(padx=10, pady=(0, 20))

        self.question = GL.StringVar()
        lab_question = GL.Label(self, textvariable=self.question,
                                foreground=GL.COL_B1, font=GL.LARGE_FONT)
        lab_question.pack()

        self.remark = GL.StringVar()
        lab_remark = GL.Label(self, textvariable=self.remark,
                              foreground=GL.COL_B1, font=GL.SMALL_FONT)
        lab_remark.pack(pady=(1, 5))

        self.useranswer = GL.StringVar()
        self.disp_answer = GL.Entry(self, textvariable=self.useranswer,
                                    foreground=GL.COL_B2, font=GL.ANSWER_FONT,
                                    justify=GL.CENTER)
        self.disp_answer.pack(fill=GL.X)

        self.symbol_indicator = GL.StringVar()
        self.lab_symbol = GL.Label(self, textvariable=self.symbol_indicator,
                                   foreground=GL.COL_FALSE, font=GL.NORMAL)
        self.lab_symbol.pack()

        self.response = GL.StringVar()
        self.disp_response = GL.Label(self, textvariable=self.response,
                                      foreground=GL.COL_B1, font=GL.MEDIUM_FONT)
        self.disp_response.pack()

        buttongroup = GL.Frame(self)
        self.but_help = GL.Button(buttongroup, text="Hilfe",
                                  command=self.hit_help)
        self.but_help.pack(side=GL.LEFT)
        self.but_enter = GL.Button(buttongroup, text="Enter",
                                   width=17,
                                   command=self.hit_enter)
        self.but_enter.pack(side=GL.LEFT)
        self.but_next = GL.Button(buttongroup, text="Weiter",
                                  command=self.hit_next)
        self.but_next.pack(side=GL.LEFT)
        buttongroup.pack(padx=10, pady=(25, 2))

        self.indicator = GL.Label(self, background=GL.COL_B3)
        self.indicator.pack(side=GL.BOTTOM, fill=GL.X, ipady=10)

        self.disp_answer.bind("<Return>", self.return_key)
        self.but_enter.bind("<Return>", self.return_key)
        self.but_help.bind("<Return>", self.give_help)

    def give_help(self, event):
        """Krücke um die Tastenbindung zur Hilfefunktion auszulösen."""
        self.hit_help()

    def hit_help(self):
        """Funktionalität der Hilfefunktion. Gesteuert durch gewählte Optionen."""
        self.hnum += 1
        if self.options[1] == 0 and self.options[2] == 1:
            self.hnum += 1
        solution = self.patience[self.pgroup][self.pgnum]["feld_2"]
        first_letter = solution[0]
        if self.hnum == 1 and self.options[1] == 1:
            self.useranswer.set(first_letter)
            self.disp_answer.icursor(1)
        elif self.hnum == 2 and self.options[2] == 1:
            self.hnum = 0
            hlen = len(solution)
            solution = solution.split()
            ldot = []
            for ele in solution:
                ele = "*" * len(ele)
                ldot.append(ele)
            dots = " ".join(ldot)
            dots = first_letter + dots[1:]
            self.useranswer.set(dots)
            if first_letter == "":
                self.disp_answer.icursor(0)
            else:
                self.disp_answer.select_range(1, hlen)

        self.disp_answer.focus_set()

    def return_key(self, event):
        """Krücke um die Tastenbindung zu Enter und Weiter auszulösen."""
        state = str(self.but_enter["state"])
        if state == GL.NORMAL:
            self.hit_enter()
        else:
            self.hit_next()

    def check_answer(self, uinput, solution, alternative):
        """Urteilt über Korrektheit der Antwort. Optionen werden einbezogen."""
        if self.options[0] == 1:
            uinput = uinput.lower()
            solution = solution.lower()
            alternative = [x.lower() for x in alternative]

        if self.options[3] == 1:
            answ1 = uinput == solution
            if len(alternative) > 0:
                answ2 = uinput in alternative
            else:
                answ2 = False
            answ = answ1 or answ2
        else:
            answ = uinput == solution

        return answ

    def hit_enter(self):
        """Funktionalität des Enter-Button. Regelt diverse Anzeigen."""
        self.but_enter.configure(state=GL.DISABLED)
        self.but_next.configure(state=GL.NORMAL)

        uanswer = self.useranswer.get()
        solution = self.patience[self.pgroup][self.pgnum]["feld_2"]
        altsolutions = self.patience[self.pgroup][self.pgnum]["alt_2"]
        answ = self.check_answer(uanswer,
                                 solution,
                                 altsolutions)
        if answ:
            if len(altsolutions) == 0:
                self.response.set(solution + " ✔")
            else:
                if self.options[3] == 1:
                    self.response.set(solution + " ✔" + " alternativ: " + ", ".join(altsolutions))
                else:
                    self.response.set(solution + " ✔")

            self.disp_answer.configure(foreground=GL.COL_CORRECT)
            self.indicator.configure(background=GL.COL_CORRECT)
            self.patience[self.pgroup][self.pgnum]["verlauf"].append([GL.time(), 1])
            self.richtige += 1
        else:
            self.disp_answer.configure(foreground=GL.COL_FALSE)
            self.response.set("✘   ☛ " + solution)
            self.indicator.configure(background=GL.COL_FALSE)
            self.disp_answer.configure(state=GL.DISABLED)
            self.patience[self.pgroup][self.pgnum]["verlauf"].append([GL.time(), 0])
            self.falsche += 1
            self.snum += 1
            symbol = "✖" * self.snum
            self.symbol_indicator.set(symbol)

        self.qcounter.set("R " + str(self.richtige) + " | F " + str(self.falsche) +
                          " | T " + str(self.korpus_len))
        self.but_enter.focus_set()

    def hit_next(self):
        """Funktionalität des Next-Button."""
        self.disp_answer.configure(foreground=GL.COL_B2, state=GL.NORMAL)
        self.but_next.configure(state=GL.DISABLED)
        self.but_enter.configure(state=GL.NORMAL)
        self.useranswer.set("")
        self.response.set("")
        self.indicator.configure(background=GL.COL_B3)
        self.hnum = 0

        if self.pgnum < (self.pgrp_len - 1):            # Subliste schon durch?
            self.pgnum += 1
        else:                                           # Wenn Subliste komplett durch
            self.pgnum = 0
            correct = 0
            for ele in self.patience[self.pgroup]:      # Anzahl Richtige der Subliste zählen
                if ele["verlauf"][-1][1] > 0:
                    correct += 1
            if correct == self.pgrp_len:                # Alle richtig in Subliste: Weiter
                self.pgroup += 1
                self.snum = 0
                self.symbol_indicator.set("")
                if self.pgroup == self.grps:            # Alle Sublisten schon durch?
                    self.pgroup = 0
                    self.save_patience()
                    self.controller.show_frame("StartPage")
                else:                                   # Noch nicht alle Sublisten durch
                    self.pgrp_len = len(self.patience[self.pgroup])

            if correct == 0:                            # Alle falsch in Subliste: Abbruch
                self.pgroup = 0
                self.save_patience()
                self.controller.show_frame("StartPage")

        if self.options[4] == 1:
            self.remark.set(self.patience[self.pgroup][self.pgnum]["bemerkung"])
        self.question.set(self.patience[self.pgroup][self.pgnum]["feld_1"])
        self.disp_answer.focus_set()

    def save_patience(self):
        """Speichert gezielt das benutzte Subthema."""
        self.korpus = [item for sublist in self.patience for item in sublist]

        fname = "data/" + self.topic + ".korp"
        rawread = GL.readfile(fname)
        korpus = GL.loads(rawread)

        for ele in korpus:
            if ele["subset"]["name"] == self.subtopic:
                ele["subset"]["data"] = self.korpus

        GL.savefile(fname, korpus)

    def submit_topic(self, topic, subtopic):
        """Funktion um über die Klasse das Thema und Subthema zu übergeben."""
        self.topic = topic
        self.subtopic = subtopic
        self.options = GL.get_options()

        self.grps = 0
        self.pgroup = 0
        self.pgnum = 0
        self.richtige = 0
        self.falsche = 0
        self.snum = 0

        GL.get_korpus(self, self.topic, self.subtopic)

        self.grps = self.korpus_len // GL.GROUP_SIZE
        self.patience = [self.korpus[i::self.grps] for i in range(self.grps)]
        self.kategorie.set(topic + ": " + subtopic)

        self.pgrp_len = len(self.patience[0])

        self.question.set(self.patience[0][0]["feld_1"])
        if self.options[4] == 1:
            self.remark.set(self.patience[0][0]["bemerkung"])
        else:
            self.remark.set("")
        self.useranswer.set("")
        self.disp_answer.focus_set()

        self.symbol_indicator.set("")
        self.but_next.configure(state=GL.DISABLED)

        self.qcounter.set("R 0 | F 0 | T " + str(self.korpus_len))









