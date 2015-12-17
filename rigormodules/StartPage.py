"""Module StartPage"""
from os import walk
import rigormodules.globals as GL

class StartPage(GL.Frame):
    """GUI und Logik für die Start-Seite."""
    def __init__(self, parent, controller):

        GL.Frame.__init__(self, parent)
        self.controller = controller
        self.topic = ""
        # self.subtopic = "leer"

        label = GL.Label(self, text="Startseite", foreground=GL.COL_B1, font=GL.LARGE_FONT)
        label.pack(padx=10, pady=25)

        korp_file = []
        for (dirpath, dirnames, filenames) in walk("data"):
            korp_file.extend(filenames)
            break
        korp_name = []
        for name in korp_file:
            element = name.find(".")
            korp_name.append(name[:element])

        opmenugroup = GL.Frame(self)
        themen = korp_name
        opt_theme = GL.StringVar()
        opmenu_theme = GL.OptionMenu(opmenugroup,
                                     opt_theme,
                                     "Thema wählen",
                                     *themen)
        opmenu_theme.pack(side=GL.LEFT)

        opt_subset = GL.StringVar()

        def update_subset(self, *args):
            """Befüllt das Subset-Dropdown, abhängig vom gewählten Thema."""
            opmenu_subset["menu"].delete(0, "end")
            fname = "data/" + opt_theme.get() + ".korp"
            rawread = GL.readfile(fname)
            korpus = GL.loads(rawread)
            new_subset = []
            for i in korpus:
                new_subset.append(i["subset"]["name"])

            for choice in new_subset:
                opmenu_subset["menu"].add_cascade(label=choice,
                                                  command=GL._setit(opt_subset, choice))

        # opt_subset.set("Subset wählen")
        opmenu_subset = GL.OptionMenu(opmenugroup,
                                      opt_subset,
                                      "Subset wählen")
        opmenu_subset.pack(side=GL.LEFT)
        opmenugroup.pack(side=GL.TOP, padx=10, pady=5)

        def enable_start(self, *args):
            """Wenn Startbereit wird der Start-Button freigegeben."""
            but_start.configure(state=GL.NORMAL)

        opt_theme.trace("w", update_subset)
        opt_subset.trace("w", enable_start)

        radiogroup = GL.Frame(self)
        spielmodi = [("Anschauen", 1), ("Patience", 2), ("Gruppiert", 3), ("Alle", 4)]
        self.opt_modes = GL.IntVar()
        self.opt_modes.set(1)
        for text, mode in spielmodi:
            radio_modes = GL.Radiobutton(radiogroup, text=text, variable=self.opt_modes, value=mode)
            radio_modes.pack(side=GL.LEFT)
        radiogroup.pack(side=GL.TOP, padx=10, pady=5)

        buttongroup = GL.Frame(self)
        but_option = GL.Button(buttongroup, text="Optionen",
                               command=lambda: self.controller.show_frame("OptionPage"))
        but_option.pack(side=GL.LEFT)

        but_start = GL.Button(buttongroup, text="Start", state=GL.DISABLED,
                              command=lambda: self.start_quiz(opt_theme, opt_subset))
        but_start.pack(side=GL.LEFT)
        buttongroup.pack(padx=10, pady=(34, 25))


        lab_author = GL.Label(self, text="✿ Alex Bösch, Dez 2015 ✿",
                              foreground=GL.COL_B2, font=GL.SMALL_FONT)
        lab_author.pack()

    def start_quiz(self, topic, subtopic):
        """Startet den gewählten Modus und übergibt Thema und Subthema."""
        top = topic.get()
        subt = subtopic.get()

        mod = self.opt_modes.get()
        if mod == 1:
            self.controller.show_frame("Anschauen")
            self.controller.frames["Anschauen"].submit_topic(top, subt)
        elif mod == 2:
            self.controller.show_frame("Patience")
            self.controller.frames["Patience"].submit_topic(top, subt)
