"""Fundamentale Klasse App und deren Instanzierung als Grundlage der Anwendung."""

import rigormodules.globals as GL

import rigormodules.StartPage as SP
import rigormodules.OptionPage as OP
import rigormodules.ModAnschauen as MA
import rigormodules.ModPatience as PA

class App(GL.Tk):
    """Grundlage um verschiedene Frames zu zeigen."""
    def __init__(self, *args, **kwargs):

        GL.Tk.__init__(self, *args, **kwargs)

        GL.Tk.iconbitmap(self, default="varia/rigoricon.ico")
        GL.Tk.title(self, "Alex' Rigor")

        container = GL.Frame(self)
        container.pack(side=GL.TOP, fill=GL.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (SP.StartPage, OP.OptionPage, MA.Anschauen, PA.Patience):
            page_name = page.__name__
            frame = page(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky=GL.NSEW)

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Findet die gewünschte Seite im Stapel und bringt diese nach Vorn."""
        frame = self.frames[page_name]
        frame.tkraise()

RIGOR = App()
RIGOR.geometry("600x275+300+300")
RIGOR.mainloop()
