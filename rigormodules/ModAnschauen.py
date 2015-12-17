"""Module Anschauen"""

import rigormodules.globals as GL

class Anschauen(GL.Frame):
    """GUI-Elemente und Logik für den Modus Anschauen."""
    def __init__(self, parent, controller):
        GL.Frame.__init__(self, parent)
        self.controller = controller

        self.topic = ""
        self.subtopic = ""
        self.korpus = []
        self.korpus_len = 0
        self.qnum = 0
        self.state = ""

        grp_titel = GL.Frame(self)
        lab_modus = GL.Label(grp_titel, text="Modus: Anschauen",
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

        self.answer = GL.StringVar()
        lab_answer = GL.Label(self, textvariable=self.answer,
                              foreground=GL.COL_B2, font=GL.ANSWER_FONT)
        lab_answer.pack()

        buttongroup = GL.Frame(self)
        but_back = GL.Button(buttongroup, text="⇦ zurück",
                             command=self.back)
        but_back.pack(side=GL.LEFT)
        but_next = GL.Button(buttongroup, text="weiter ⇨",
                             command=self.next)
        but_next.pack(side=GL.LEFT)
        buttongroup.pack(padx=10, pady=(25, 2))
        but_home = GL.Button(self, text="Startseite",
                             width=24,
                             command=lambda: self.controller.show_frame("StartPage"))
        but_home.pack()

    def next(self):
        """Funktionalität des Weiter-Buttons."""
        if self.state == "show":
            self.answer.set(self.korpus[self.qnum]["feld_2"])
            self.state = "next"
        else:
            if self.qnum == (self.korpus_len - 1):
                self.qnum = -1
            self.qnum += 1
            self.qcounter.set(str(self.qnum + 1) + " von " + str(self.korpus_len))
            self.question.set(self.korpus[self.qnum]["feld_1"])
            self.remark.set(self.korpus[self.qnum]["bemerkung"])
            self.answer.set("")
            self.state = "show"

    def back(self):
        """Funktionalität des Zurück-Buttons."""
        # TODO: Umkehrung der Frage-Antwort Reihenfolge!
        if self.state == "next":
            self.answer.set("")
            self.remark.set(self.korpus[self.qnum]["bemerkung"])
            self.state = "show"
        else:
            if self.qnum == 0:
                self.qnum = self.korpus_len
            self.qnum -= 1
            self.qcounter.set(str(self.qnum + 1) + " von " + str(self.korpus_len))
            self.question.set(self.korpus[self.qnum]["feld_1"])
            self.answer.set(self.korpus[self.qnum]["feld_2"])
            self.remark.set(self.korpus[self.qnum]["bemerkung"])
            self.state = "next"

    def submit_topic(self, topic, subtopic):
        """Funktion um über die Klasse das Thema und Subthema zu übergeben."""
        self.topic = topic
        self.subtopic = subtopic

        GL.get_korpus(self, self.topic, self.subtopic)

        self.kategorie.set(topic + ": " + subtopic)

        self.state = "show"
        self.qnum = 0

        self.question.set(self.korpus[0]["feld_1"])
        self.remark.set(self.korpus[0]["bemerkung"])
        self.answer.set("")

        self.qcounter.set("1 von " + str(self.korpus_len))






