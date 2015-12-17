"""Alle Importe, globale Funktionen und globale Variablen (Konstanten)
liegen hier zentralisiert."""

from tkinter import Tk, IntVar, StringVar, _setit
from tkinter import NSEW, TOP, RIGHT, LEFT, BOTTOM, CENTER, BOTH, DISABLED, NORMAL, X, Y
from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, Radiobutton, OptionMenu

from json import loads, dumps
from time import time

LARGE_FONT = ("Verdana", 14)
ANSWER_FONT = ("Verdana", 20, "bold")
MEDIUM_FONT = ("Verdana", 12)
MEDIUM_FONT_2 = ("Verdana", 12, "bold")
SMALL_FONT = ("Verdana", 8)

COL_B1 = "grey20"
COL_B2 = "grey40"
COL_B3 = "grey75"
COL_NEUTRAL = "grey94"
COL_CORRECT = "green"
COL_FALSE = "red"

GROUP_SIZE = 4  # Für Patience-Mode

def readfile(filename):
    """Einfaches Lesen aus File"""
    with open(filename, encoding="utf-8") as file:
        raw = file.read()
    return raw

def savefile(filename, data):
    """Speichert Daten in File als JSON-Dump"""
    with open(filename, "w", encoding="utf-8") as file:
        output = dumps(data, ensure_ascii=False, sort_keys=True, indent=2)
        file.write(output)

def get_options():
    rawread = readfile("varia/options.opt")
    return loads(rawread)

def get_korpus(self, topic, subset):
    rawread = readfile("data/" + topic + ".korp")
    kall = loads(rawread)
    for ele in kall:
        if ele["subset"]["name"] == subset:
            self.korpus = ele["subset"]["data"]
    self.korpus_len = len(self.korpus)
    