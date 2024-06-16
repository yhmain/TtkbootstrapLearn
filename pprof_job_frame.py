import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from threading import Thread
from ttkbootstrap.dialogs.dialogs import MessageDialog, Messagebox
from ttkbootstrap.window import Toplevel
from tkinter.scrolledtext import ScrolledText

from datetime import datetime

from tool_pprof import ToolPprof


class PprofJob(ttk.Frame):

    def __init__(self, master, pod_type, pod_ip, curl_type, con_type):
        super().__init__(master.prog_frame)
        self.pack(fill=X, expand=YES, pady=3)

        self.master = master
        self.job_id = (pod_type, con_type, curl_type)
        self.master.job_set_add(self.job_id)
        self.complete_flag = False      # 标识任务是否彻底完成，并且该组件可以删除

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.curl_pod_info = "Pod:{0} 容器:{1} 采集类型:{2} 开始时间:{3}".format(pod_type, con_type, curl_type, now_str)
        self.curl_pod_label = ttk.Label(self, text=self.curl_pod_info, bootstyle='info')
        self.curl_pod_label.pack(side=LEFT, padx=(0, 15))

        self.md_str = self.curl_pod_info
        # self.md = MessageDialog(self.md_str, title=self.curl_pod_info, buttons=["OK"])

        self.progressbar = ttk.Progressbar(
            master=self,
            mode=DETERMINATE,
            bootstyle=(STRIPED, SUCCESS),
            maximum=100,    # 设置进度条最大值为100
        )
        self.progressbar.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)  # 通过fill=BOTH和expand=YES参数，ProgressBar会填满剩余的水平和垂直空间

        self.create_progress_detail()        # 首先创建出日志弹窗，但是不显示

        self.progress_val_show = ttk.Button(self, text="Progress: 0%", bootstyle='success', command=self.show_progress_detail)
        self.progress_val_show.pack(side=LEFT, padx=(0, 5))

        self.btn_download = ttk.Button(self, text="点击下载", state="disable", bootstyle="info", command=self.download_pprof)
        self.btn_download.pack(side=LEFT, padx=(0, 15))     # active, normal

        self.tool_pprof = ToolPprof()

        # start search in another thread to prevent UI from locking
        self.p_step = 0
        self.progressbar.step(self.p_step)
        Thread(
            target=self.tool_pprof.do_curl_job,
            args=(pod_type, pod_ip, curl_type),
            daemon=True
        ).start()
        self.progressbar.start(1000)
        self.after(1000, lambda: self.check_progress())

    def check_progress(self):
        end, val, info = self.tool_pprof.is_finished_job()
        self.progressbar['value'] = val
        self.progress_val_show.config(text="Progress: {0}%".format(val))
        # self.md_str += "\n" + info      # 初始化加载使用
        self.textbox.insert("end", "\n" + info)
        self.textbox.see("end")     # 使用 see('end') 方法确保滚动条始终显示在最后一行
        if end:
            self.progressbar.stop()
            self.btn_download.config(state="active")
            self.master.job_set_del(self.job_id)
            self.complete_flag = True
        else:
            # self.update_idletasks()
            self.after(1000, lambda: self.check_progress())

    def cancel_close_top(self):
        def on_closing():
            Messagebox.show_warning("不要点'x'来关闭，请点击下面的退出来关闭该窗口！")
            pass  # 空操作，不做任何处理，所以窗口不会关闭

        self.top.protocol("WM_DELETE_WINDOW", on_closing)

    def create_progress_detail(self):
        self.top = Toplevel()
        self.top.title(self.curl_pod_info)
        self.cancel_close_top()

        label = ttk.Label(self.top, text='本次日志如下', bootstyle=SUCCESS)
        label.pack()
        style = ttk.Style()
        self.textbox = ScrolledText(
            master=self.top,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1
        )
        self.textbox.pack(fill=BOTH)
        self.textbox.insert(END, self.md_str)

        last_row = ttk.Frame(self.top)
        last_row.pack()
        last_btn = ttk.Button(last_row, text="退出", command=self.top.withdraw)       # 取消显示
        last_btn.pack(side=RIGHT, fill=X, padx=15, pady=15)
        self.top.withdraw()     # 暂且不显示

    def show_progress_detail(self):
        self.top.deiconify()        # 显示

    def download_pprof(self):
        md = Messagebox.ok(self.curl_pod_info, "下载pprof")
        md.show()
        # md = MessageDialog("Displays a message with buttons.", buttons=["OK"])

