import os.path
from pathlib import Path
from tkinter import PhotoImage

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

PATH_DIR = Path(__file__).parent


class TtkbMain(ttk.Frame):
    BASE_DIR = os.path.abspath(__file__)
    # print(BASE_DIR)

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        self.images = [
            PhotoImage(
                name="pprof",
                file=PATH_DIR / 'images/pprof2.jpg'
            ),
            PhotoImage(
                name="pprof2",
                file=PATH_DIR / 'images/pprof2.jpg'
            )
        ]

        print(type(TtkbMain.BASE_DIR), TtkbMain.BASE_DIR)
        self.btn_pprof_demo = ttk.Button(self, text="pprof采集工具的Demo", image="pprof2", bootstyle="info-link")
        # self.btn_pprof_demo.pack(fill=X, expand=YES, anchor=CENTER)
        self.btn_pprof_demo.grid(row=2, column=2, rowspan=2, columnspan=2)

        self.btn_pprof_demo2 = ttk.Button(self, text="pprof采集工具的Demo222", image="pprof2", bootstyle="info-link")
        self.btn_pprof_demo2.grid(row=2, column=4, rowspan=2, columnspan=2)

        # self.func_label = ttk.Label(self, image="")

