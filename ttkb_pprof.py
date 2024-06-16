import threading

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs.dialogs import MessageDialog, Messagebox

from tool_pprof import ToolPprof
from pprof_job_frame import PprofJob


class TtkbPprof(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        self.job_frame_id = set()
        self.job_id_set = set()     # 当前正在运行的任务
        self._lock_job_id = threading.Lock()
        # self._lock_job_frame_id = threading.Lock()

        self.container_type = ttk.Labelframe(self, text="采集的容器类型", padding=5)
        self.container_type.pack(fill=X, expand=YES, anchor=N)
        self.config_container_type()  # 提前声明好相关组件

        self.node_info = ttk.Labelframe(self, text="容器所在节点信息", padding=5)
        self.node_info.pack(fill=X, expand=YES, anchor=N)
        self.config_node_info()  # 提前声明好相关组件

        self.create_container_type()

        self.start_curl = ttk.Labelframe(self, text="pprof采集进度")
        self.start_curl.pack(fill=X, expand=YES, anchor=N)

        self.config_start_curl()

        # self.log_scroll = ScrolledText(self, padding=5, height=100)
        # self.log_scroll.pack(fill=BOTH, expand=YES, anchor=N)
        # self.log_scroll.insert("end", 'Insert your text here.')

    def config_container_type(self):
        self.pod_con_map = ToolPprof().get_pod_con_map()  # 数据获取源头

        self.con_combox_val = list(self.pod_con_map.keys())
        self.con_text_var = ttk.StringVar(value=self.con_combox_val[0])

        self.pod_combox_val = self.pod_con_map[self.con_combox_val[0]]
        self.pod_text_var = ttk.StringVar(value=self.pod_combox_val[0])

        final_info = "你的选择为Pod: {0} 容器：{1}".format(self.pod_combox_val[0], self.con_combox_val[0])
        self.final_text_var = ttk.StringVar(value=final_info)

    def config_node_info(self):
        self.node_table = Tableview(
            master=self.node_info,
            coldata=ToolPprof().get_node_columns(),
            # rowdata=ToolPprof().get_node_rows_data(),
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            # stripecolor=(colors.light, None),
            pagesize=10,
        )
        self.node_table.pack(fill=BOTH, expand=YES, pady=10)

        self.node_select_txt = ttk.StringVar(value="你的选择为:")

        def show_all_selected():
            selected_row = self.node_table.get_rows(selected=True)  # 获取选中的行索引
            show_txt = "你的选择为:" + ",".join([e.values[0] for e in selected_row])
            self.node_select_txt.set(show_txt)
            print(self.node_select_txt.get())

        # node_btn_selected = ttk.Button(self.node_info, text="查看所有选中", command=show_all_selected)
        # node_btn_selected.pack(side=LEFT, fill=X, expand=YES, padx=10)
        #
        # node_label = ttk.Label(self.node_info, textvariable=self.node_select_txt)
        # node_label.pack(side=LEFT, fill=X, expand=YES, padx=15)

    def create_container_type(self):
        con_frame = ttk.Frame(self.container_type)
        con_frame.pack(fill=X, expand=YES)
        con_type = ttk.Label(con_frame, text="容器类型：", width=10)
        con_type.pack(side=LEFT, padx=(15, 0))
        con_combox = ttk.Combobox(con_frame, bootstyle=INFO, values=self.con_combox_val, state=READONLY,
                                  textvariable=self.con_text_var)
        con_combox.pack(side=LEFT, fill=X, expand=YES, padx=5)

        pod_type = ttk.Label(con_frame, text="Pod类型：", width=10)
        pod_type.pack(side=LEFT, padx=(15, 0))
        pod_combox = ttk.Combobox(con_frame, bootstyle=INFO, state=READONLY, values=self.pod_combox_val,
                                  textvariable=self.pod_text_var)
        pod_combox.pack(side=LEFT, fill=X, expand=YES, padx=5)

        def pod_combox_selected(event):
            con_txt = self.con_text_var.get()
            pod_txt = self.pod_text_var.get()
            final_info = "你的选择为Pod: {0} 容器：{1}".format(pod_txt, con_txt)
            self.final_text_var.set(final_info)

        def con_combox_selected(event):
            new_pod_val = self.pod_con_map[self.con_text_var.get()]  # 获取对应的新数据
            pod_combox.config(values=new_pod_val)  # 更新下拉列表
            pod_combox.set(new_pod_val[0])  # 设置选中项
            pod_combox_selected(event)  # 更新文本框内容

        con_combox.bind('<<ComboboxSelected>>', con_combox_selected)
        pod_combox.bind('<<ComboboxSelected>>', pod_combox_selected)

        con_label = ttk.Label(con_frame, textvariable=self.final_text_var)
        con_label.pack(side=LEFT, fill=X, expand=YES, padx=5)

        find_node_btn = ttk.Button(con_frame, text="查询节点信息", command=self.fill_node_table)
        find_node_btn.pack(side=LEFT, fill=X, expand=YES, padx=5)

    def fill_node_table(self):
        pod_type = self.pod_text_var.get()
        row_datas = ToolPprof().get_node_rows_data(pod_type)
        self.node_table.delete_rows()  # 清空数据
        self.node_table.insert_rows('end', row_datas[::-1])  # 批量插入数据，逆序插入则顺序显示
        self.node_table.load_table_data()  # 加载数据，使数据显示在表格中

    def config_start_curl(self):
        curl_frame = ttk.Frame(self.start_curl)
        curl_frame.pack(fill=X, expand=YES)
        curl_type = ttk.Label(curl_frame, text="采集类型：", width=10)
        curl_type.pack(side=LEFT, padx=(15, 0))

        combox_data = ToolPprof().get_pprof_type()
        self.curl_type_txt = ttk.StringVar(value=combox_data[0])
        curl_combox = ttk.Combobox(curl_frame, bootstyle=INFO, values=combox_data, state=READONLY,
                                   textvariable=self.curl_type_txt)
        curl_combox.pack(side=LEFT, fill=X, expand=YES, padx=5)

        final_info = "你选择的采集类型为：{0}".format(self.curl_type_txt.get())
        self.final_curl_txt = ttk.StringVar(value=final_info)
        con_label = ttk.Label(curl_frame, textvariable=self.final_curl_txt)
        con_label.pack(side=LEFT, fill=X, expand=YES, padx=5)

        curl_btn = ttk.Button(curl_frame, text="开始采集", command=self.do_curl)
        curl_btn.pack(side=LEFT, fill=X, expand=YES, padx=5)

        clear_job_btn = ttk.Button(curl_frame, text="清理任务", command=self.do_clear)
        clear_job_btn.pack(side=LEFT, fill=X, expand=YES, padx=5)

        self.prog_frame = ScrolledFrame(self.start_curl, autohide=True)
        self.prog_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        def curl_combox_selected(event):
            curl_txt = self.curl_type_txt.get()
            final_info = "你选择的采集类型为：{0}".format(curl_txt)
            self.final_curl_txt.set(final_info)

        curl_combox.bind('<<ComboboxSelected>>', curl_combox_selected)

    def do_curl(self):
        selected_row = self.node_table.get_rows(selected=True)  # 获取选中的行索引
        if len(selected_row) < 1:       # 未选中一行
            Messagebox.ok("请至少选中一行数据！", "采集pprof")
            return
        selected_pods = [(e.values[0], e.values[5]) for e in selected_row]

        for pod_type, pod_ip in selected_pods:
            con_type = self.con_text_var.get()
            curl_type = self.curl_type_txt.get()

            temp_item = (pod_type, con_type, curl_type)
            if self.job_set_contains(temp_item):
                Messagebox.ok("任务：{0} 正在运行中，不可创建重复任务！".format("Pod:{0} 容器:{1} 采集类型:{2}".format(pod_type, con_type, curl_type)))
                continue

            PprofJob(self, pod_type, pod_ip, curl_type, con_type)

    def do_clear(self):
        clear_w = list()
        for child in self.prog_frame.winfo_children():
            if child.complete_flag:
                clear_w.append(child)
                # child.pack_forget()  # 如果子组件使用的是pack布局，使用pack_forget删除
                # 如果子组件使用的是grid或place布局，请使用grid_forget或place_forget
        if len(clear_w) < 1:
            Messagebox.ok("当前无可清理任务！")
            return

        msg = "是否清理如下任务（数量：{0}）：\n".format(len(clear_w))
        msg += "\n".join([e.curl_pod_info for e in clear_w])
        # md = MessageDialog(msg, "清理任务")
        choice = Messagebox.show_question(msg, "清理任务",  actions=[
            ('Yes', 'yes'),
            ('No', 'no')
        ])
        print("choice: ", choice)
        if choice in ["确认", "ok", "yes"]:
            for c in clear_w:
                print("清理任务：", " Task:", c.curl_pod_info)
                c.pack_forget()     # 相当于隐藏
                c.destroy()         # 销毁

    def job_set_add(self, item):
        # item长度为2， item[0]:组件的标识元组  item[1]: 组件的widget_id
        with self._lock_job_id:
            self.job_id_set.add(item)
            print(self.job_id_set)

    def job_set_del(self, item):
        with self._lock_job_id:
            self.job_id_set.remove(item)
            print(self.job_id_set)

    def job_set_contains(self, item):
        with self._lock_job_id:
            return item in self.job_id_set
