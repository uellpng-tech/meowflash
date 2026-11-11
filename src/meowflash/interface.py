import tkinter as tk
import sys
import os
import threading
from tkinter import ttk, Scrollbar, PhotoImage
from src.meowflash import hardware

def ini_interface():
    global criar_aba, note, excluir_aba

    janela = tk.Tk()
    janela.title("MeowFlesh")
    janela.geometry("450x500")
    if sys.platform.startswith("win32"):
        janela.bitmap(file="assets/icon.ico")
    janela.minsize(450, 500)
    janela.maxsize(450, 500)
    janela.config(background="#1F1F1F")

    es = ttk.Style(janela)
    es.theme_use("clam")
    es.configure("TNotebook", background="#1F1F1F", bordercolor="#1B1B1B", lightcolor="#111111", darkcolor="#111111")
    es.configure("InteriorAba.TFrame", background="#1B1B1B", bordercolor="#1B1B1B")
    es.configure("TNotebook.Tab", foreground="#000000", background="#1B1B1B", bordercolor="#111111", lightcolor="#111111")
    es.map(style="TNotebook.Tab", background=[("selected", "#1B1B1B"), ("active", "#2B2A2A")], bordercolor=[("selected", "#111111"), ("active", "#111111")], lightcolor=[("active", "#111111"), ("selected", "#111111")])
    
    note = ttk.Notebook(janela, width=400, height=450, style="TNotebook")
    note.place(x=25, y=2)

    aba_geral = ttk.Frame(note, style="InteriorAba.TFrame")
    note.add(aba_geral, text="Geral")

    def criar_aba(lista):

        for abas in lista:
            aba = ttk.Frame(note, style="InteriorAba.TFrame")
            note.add(aba, text=f"{abas["Label"]}")

    def excluir_aba(lista, local):
            note.forget(f"{lista[local]["Label"]}")

    def close():
        hardware.close()
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", close)
    janela.mainloop()