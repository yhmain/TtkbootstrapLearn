import datetime
import pathlib
from queue import Queue
from threading import Thread
from tkinter.filedialog import askdirectory
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility

from demo import FileSearchEngine


if __name__ == '__main__':

    app = ttk.Window("File Search Engine", "journal")
    FileSearchEngine(app)
    app.mainloop()
