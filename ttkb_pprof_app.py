import copy

import ttkbootstrap as ttk
from ttkbootstrap.themes.standard import STANDARD_THEMES
from ttkbootstrap import Style

from ttkb_pprof import TtkbPprof


class UiPprof:
    def __init__(self):
        self.app = ttk.Window("TestApp Tool")
        self.style = Style(theme="flatly")     # 开局默认的主题
        self.create_menubar()
        TtkbPprof(self.app)

    def run(self):
        self.app.mainloop()

    def create_menubar(self):
        menubar = ttk.Menu(self.app)
        theme_menu = ttk.Menu(menubar)  # 新增一个主题菜单
        menubar.add_cascade(label="主题", menu=theme_menu)

        theme_menu_sub = ttk.Menu(theme_menu)
        theme_menu.add_cascade(label="切换主题", menu=theme_menu_sub, underline=0)
        th_list = list(STANDARD_THEMES.keys())
        for i in range(len(th_list)):  # 遍历所有主题
            print("th: ", th_list[i])
            theme_menu_sub.add_command(label=th_list[i], command=lambda th=th_list[i]: self.style.theme_use(th))
            # theme_menu_sub.add_command(label=th_list[i], command=lambda: self.switch_theme(th_list[i]))       # 实现失败！

        # l = list(STANDARD_THEMES.keys())
        # theme_menu_sub.add_command(label="test1", command=lambda: self.switch_theme(l[0]))
        # theme_menu_sub.add_command(label="test2", command=lambda: self.switch_theme(l[1]))

        about_menu = ttk.Menu(menubar)  # 新增一个关于菜单
        menubar.add_cascade(label="关于", menu=about_menu)

        menubar.add_command(label="退出", command=self.app.quit)

        self.app.config(menu=menubar)


UiPprof().run()
