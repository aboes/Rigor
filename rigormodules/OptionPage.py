"""Alles was die Konfiguration betrifft."""

import rigormodules.globals as GL

class OptionPage(GL.Frame):
    """GUI und Logik für die Options-Seite. Gewählte Optionen werden
    beim Verlassen on-the-fly gespeichert."""
    def __init__(self, parent, controller):

        self.controller = controller
        GL.Frame.__init__(self, parent)

        self.options = GL.get_options()

        self.var_capitalize = GL.IntVar()
        self.var_hilfe1 = GL.IntVar()
        self.var_hilfe2 = GL.IntVar()
        self.var_hilfe3 = GL.IntVar()
        self.var_alternative = GL.IntVar()
        self.var_bemerkungen = GL.IntVar()
        self.var_time = GL.IntVar()

        self.var_capitalize.set(self.options[0])
        self.var_hilfe1.set(self.options[1])
        self.var_hilfe2.set(self.options[2])
        self.var_alternative.set(self.options[3])
        self.var_bemerkungen.set(self.options[4])
        self.var_hilfe3.set(self.options[5])
        self.var_time.set(self.options[6])

        label = GL.Label(self, text="Optionen", font=GL.LARGE_FONT)
        label.pack(padx=10, pady=25)

        bgrp_outer = GL.Frame(self)
        bgrp_1 = GL.Frame(bgrp_outer)
        bgrp_2 = GL.Frame(bgrp_outer)

        check_capitalize = GL.Checkbutton(bgrp_1, text="Grossschreibung ignorieren",
                                          variable=self.var_capitalize, width=35)
        check_capitalize.pack()
        check_hilfe1 = GL.Checkbutton(bgrp_1, text="1. Hilfe: Ersten Buchstaben anzeigen",
                                      variable=self.var_hilfe1, width=35)
        check_hilfe1.pack()
        check_hilfe2 = GL.Checkbutton(bgrp_1, text="2. Hilfe: Anzahl Buchstaben anzeigen",
                                      variable=self.var_hilfe2, width=35)
        check_hilfe2.pack()
        check_hilfe3 = GL.Checkbutton(bgrp_1, text="3. Hilfe: Karte/Bild anzeigen",
                                      variable=self.var_hilfe3, width=35, state=GL.DISABLED)
        check_hilfe3.pack()
        check_alternative = GL.Checkbutton(bgrp_2, text="Alternative Schreibungen zulassen",
                                           variable=self.var_alternative, width=35)
        check_alternative.pack()
        check_bemerkungen = GL.Checkbutton(bgrp_2, text="Bemerkungen anzeigen",
                                           variable=self.var_bemerkungen, width=35)
        check_bemerkungen.pack()
        check_time = GL.Checkbutton(bgrp_2, text="Zeitbeschränkung (5 Sekunden)",
                                    variable=self.var_time, width=35, state=GL.DISABLED)
        check_time.pack()

        bgrp_1.pack(side=GL.LEFT)
        bgrp_2.pack(side=GL.LEFT)
        bgrp_outer.pack()

        button = GL.Button(self, text="zurück",
                           command=self.save_and_back)
        button.pack(padx=10, pady=25)

    def save_and_back(self):
        """Automatisches Sichern beim Verlassen."""
        self.options = [
            self.var_capitalize.get(),
            self.var_hilfe1.get(),
            self.var_hilfe2.get(),
            self.var_alternative.get(),
            self.var_bemerkungen.get(),
            self.var_hilfe3.get(),
            self.var_time.get()]

        GL.savefile("varia/options.opt", self.options)
        self.controller.show_frame("StartPage")
