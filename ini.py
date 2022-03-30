from processing import log_handler as lh, database as db
from win32api import GetSystemMetrics
from src.login import LoginFrame
from tkinter import *
from common import (
    M_FONT,
    M_COLOR,
    resource_path,
    set_appwindow,
    change_key,
    del_win,
)


class Login(Tk):
    def __init__(self):
        super().__init__()
        # self.master = master
        self.width = 228
        self.height = 512
        self.x, self.y = int(GetSystemMetrics(0) / 2 - self.width / 2), int(
            GetSystemMetrics(1) / 2 - self.height / 2
        )
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))
        self.iconbitmap(resource_path("images/icon.ico"))
        # self.attributes('topmost', 1)
        self.overrideredirect(1)
        self.resizable(0, 0)
        self["bg"] = M_COLOR["cbg"]
        self.title("")
        self.logger = lh.Logger()
        self.logger.log_it("kern", "info", "Application started.")
        set_appwindow(self)

        # Variables.
        self.login_frame = LoginFrame(master=self)
        self._off_set_x = 0
        self._off_set_y = 0

        # Buttons.
        self.quit_bt = Button(self.master, width=6, height=1, bd=0, text="Sair", pady=0)
        self.quit_bt["activebackground"] = M_COLOR["cbg"]
        self.quit_bt["activeforeground"] = M_COLOR["txt"]
        self.quit_bt["foreground"] = M_COLOR["txt"]
        self.quit_bt["bg"] = M_COLOR["cbg"]
        self.quit_bt["command"] = self.f_quit
        self.quit_bt["font"] = M_FONT
        self.quit_bt.place(x=86, y=488)

        # Background.
        init_bg = PhotoImage(file=resource_path("images/init_back.png"))
        self.background = init_bg
        self.bg_label = Label(self, width=226, height=200)
        self.bg_label["bg"] = M_COLOR["cbg"]
        self.bg_label["image"] = init_bg
        self.bg_label.place(x=-1, y=-2)

        # Window Movement.
        self.bg_label.bind("<Button-1>", self.click_win)
        self.bg_label.bind("<B1-Motion>", self.drag_win)
        self.bind("<Escape>", self.f_quit)

    def drag_win(self, event):
        self.x = self.winfo_pointerx() - self._off_set_x
        self.y = self.winfo_pointery() - self._off_set_y
        self.geometry("+{x}+{y}".format(x=self.x, y=self.y))
        return event

    def click_win(self, event):
        self._off_set_x = event.x
        self._off_set_y = event.y

    def f_quit(self, event=None):
        self.quit_bt["text"] = "Saindo..."
        self.quit_bt["foreground"] = M_COLOR["error"]
        self.logger.log_it("kern", "info", "Application ended.")
        self.after(250, self.destroy)
        return event


def login():
    db.create_db()
    change_key()
    root = Login()
    root.protocol("WM_DELETE_WINDOW", lambda: del_win(root))
    root.mainloop()


if __name__ == "__main__":
    # Uma variável interna do python vai receber __main__
    # se o script for rodado -> python ini.py
    # recebendo um valor diferente caso seja importada.
    login()
