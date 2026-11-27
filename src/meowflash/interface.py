import tkinter as tk
import sys
import os
import threading
from tkinter import ttk, Scrollbar, PhotoImage
from src.meowflash import hardware
from PIL import Image, ImageTk

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

    canvas = tk.Canvas(aba_geral, background="#1B1B1B", highlightthickness=0, borderwidth=0)
    canvas.pack(fill="both", expand=True)

    frame_scroll = ttk.Frame(canvas, style="InteriorAba.TFrame", width=400, height=2000)

    canvas_id = canvas.create_window(0, 0, window=frame_scroll, anchor="nw")

    es.configure("Vertical.TScrollbar", background="#1B1B1B", troughcolor="#1D1D1D", bordercolor="#111111", lightcolor="#111111", darkcolor="#111111")
    es.map(style="Vertical.TScrollbar", background=[("active", "#1B1B1B")])

    scrolada = ttk.Scrollbar(janela, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
    scrolada.pack(side="right", ipady=350, padx=10, pady=(32, 16))
    canvas.config(yscrollcommand=scrolada.set, scrollregion=(0, 0, 400, 2000))

    def scroll(event):
        canvas.itemconfig(canvas_id, width=event.width)

    canvas.bind("<Configure>", scroll)

    atalhos = []

    def criar_aba(dic):
        global note, img_atalho

        aba = ttk.Frame(note, style="InteriorAba.TFrame")
        note.add(aba, text=f"{dic["Modelo"]}")

        def entrar():
            note.select(aba)

        img_atalho_pil = Image.open("src/meowflash/assets/img-usb.png")
        img_atalho_pilf = img_atalho_pil.resize((42, 42))
        img_atalho = ImageTk.PhotoImage(img_atalho_pilf)

        btn_aba = ttk.Button(frame_scroll, image=img_atalho, command=entrar, compound= tk.LEFT)
        btn_aba.pack(fill="x", ipady=40)

        atalhos.append(btn_aba)

    def excluir_aba(remover):
        global note

        local = 0

        for id in note.tabs():
            if note.tab(id, "text") == f"{remover}":
                note.forget(id)
                atalhos[local-1].destroy()
                atalhos.pop(local-1)
            else:
                local += 1

    janela.protocol("WM_DELETE_WINDOW", janela.destroy)
    janela.mainloop()