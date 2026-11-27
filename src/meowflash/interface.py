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
    es.configure("InteriorAba.TFrame", background="#1B1B1B")
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
    bordas = []

    def criar_aba(dic):
        global note, img_atalho, img_pen

        aba = ttk.Frame(note, style="InteriorAba.TFrame")
        note.add(aba, text=f"{dic["Modelo"]}")

        def entrar():
            note.select(aba)

        es.configure("InteriorAbabtn.TFrame", background="#1B1B1B")
        es.configure("Borda.TFrame", background="#111111")

        btn_aba = ttk.Frame(frame_scroll, style="InteriorAbabtn.TFrame")
        btn_aba.pack(fill="x", ipady=70)
        btn_aba.bind("<Button-1>", lambda event: entrar())

        borda_aba = ttk.Frame(frame_scroll, style="Borda.TFrame", height=2)
        borda_aba.pack(fill="x")
        borda_aba.pack_propagate(False)

        pen_img = Image.open("src/meowflash/assets/img-usb.png")
        pen_imgf = pen_img.resize((100, 100))
        img_pen = ImageTk.PhotoImage(pen_imgf)

        img_label = tk.Label(btn_aba, image=img_pen, bg="#1B1B1B")
        img_label.place(x=10, y=10)

        atalhos.append(btn_aba)
        bordas.append(borda_aba)

    def excluir_aba(remover):
        global note

        local = 0

        for id in note.tabs():
            if note.tab(id, "text") == f"{remover}":
                note.forget(id)
                atalhos[local-1].destroy()
                bordas[local-1].destroy()
                atalhos.pop(local-1)
                bordas.pop(local-1)
            else:
                local += 1

    def close():
        janela.destroy()
        hardware.close()

    janela.protocol("WM_DELETE_WINDOW", close)
    janela.mainloop()