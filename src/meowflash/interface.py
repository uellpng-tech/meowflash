import tkinter as tk
import sys
import os
import threading
import matplotlib.pyplot as plt
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

    pen_img = Image.open("src/meowflash/assets/img-usb.png")
    pen_imgf = pen_img.resize((130, 130))
    img_pen = ImageTk.PhotoImage(pen_imgf)

    def criar_aba(dic):
        global note

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

        img_label = tk.Label(btn_aba, image=img_pen, bg="#1B1B1B")
        img_label.place(x=9, y=2)
        img_label.bind("<Button-1>", lambda event: entrar())

        linha = tk.Frame(btn_aba, height=108, width=1, bg="#111111")
        linha.place(x=150, y=14)
        linha.bind("<Button-1>", lambda event: entrar())

        es.configure("Titulo.TLabel", font=("Arial", 10, "bold"), background="#1B1B1B", foreground="#383838")
        es.configure("Info.TLabel", font=("Arial", 8), background="#1B1B1B", foreground="#383838")

        fabricantet = ttk.Label(btn_aba, text="Fabricante:", style="Titulo.TLabel")
        fabricantei = ttk.Label(btn_aba, text=dic["Fabricante"], style="Info.TLabel")
        fabricantet.place(x=160, y=14)
        fabricantei.place(x=230, y=16.5)
        fabricantet.bind("<Button-1>", lambda event: entrar())
        fabricantei.bind("<Button-1>", lambda event: entrar())

        modelot = ttk.Label(btn_aba, text="Modelo:", style="Titulo.TLabel")
        modeloi = ttk.Label(btn_aba, text=dic["Modelo"], style="Info.TLabel")
        modelot.place(x=160, y=33)
        modeloi.place(x=212, y=35.5)
        modelot.bind("<Button-1>", lambda event: entrar())
        modeloi.bind("<Button-1>", lambda event: entrar())

        snt = ttk.Label(btn_aba, text="N/S:", style="Titulo.TLabel")
        sni = ttk.Label(btn_aba, text=dic["Número de Série"], style="Info.TLabel")
        snt.place(x=160, y=52)
        sni.place(x=190, y=54.5)
        snt.bind("<Button-1>", lambda event: entrar())
        sni.bind("<Button-1>", lambda event: entrar())

        for particoes in dic["Partições"]:
            plt.barh(particoes["Label"], particoes["Tamanho"])

        tamanhot = ttk.Label(btn_aba, text="Tamanho:", style="Titulo.TLabel")
        tamanhoi = ttk.Label(btn_aba, text=dic["Tamanho"], font=("Arial", 10), background="#1B1B1B", foreground="#383838")
        tamanhot.place(x=160, y=100)
        tamanhoi.place(x=227, y=100)
        tamanhot.bind("<Button-1>", lambda event: entrar())
        tamanhoi.bind("<Button-1>", lambda event: entrar())

        caminhot = ttk.Label(btn_aba, text="Caminho:", style="Titulo.TLabel")
        caminhoi = ttk.Label(btn_aba, text=dic["Caminho"], style="Info.TLabel")
        caminhot.place(x=270, y=100)
        caminhoi.place(x=335, y=102.5)
        caminhot.bind("<Button-1>", lambda event: entrar())
        caminhoi.bind("<Button-1>", lambda event: entrar())

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