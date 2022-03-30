from common import M_FONT, M_COLOR, resource_path, del_win
from processing.log_handler import Logger
from win32api import GetSystemMetrics
from src.accounting import Accounting
from src.toolbar import Toolbar
from src.profile import Profile
from tkinter import *


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self["bg"] = M_COLOR["darker"]
        self.pack_propagate(False)
        self["height"] = 22
        self["width"] = 764
        self.customer = self.master.customer
        # Labels.
        self.status_lb = Label(
            self,
            text=f"Olá, {self.customer.name} - Constancy",
            bg=M_COLOR["darker"],
            fg=M_COLOR["txt"],
            font=M_FONT,
        )
        self.status_lb.pack(side=LEFT, padx=4)
        self.version_lb = Label(
            self, text="2.0 (WIP)", bg=M_COLOR["darker"], fg=M_COLOR["txt"], font=M_FONT
        )
        self.version_lb.pack(side=RIGHT, padx=4)

        # master.title()
        self.status_lb.configure(text="Iniciado")


# MainWindow window.
class MainWindow(Toplevel):
    def __init__(self, master, customer):
        super().__init__()
        self.master = master
        self.customer = customer
        self.logger = Logger()
        self.res_w, self.res_h = 764, 286  # carregar do arquivo de usuarios
        self.x, self.y = int(GetSystemMetrics(0) / 2 - self.res_w / 2), int(
            GetSystemMetrics(1) / 2 - self.res_h / 2
        )
        self.geometry(f"{self.res_w}x{self.res_h}+{self.x}+{self.y}")
        self.iconbitmap(resource_path("images/icon.ico"))
        self.focus_force()
        # self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", lambda: del_win(self.master))
        self.logger.log_it("kern", "info", "Main window opened.")

        # Variables.
        # self.res_before = self.res_w, self.res_h
        self.frame_on_top = "accounting"
        self.loc_before = self.winfo_x(), self.winfo_y()
        self.window_status = "normal"
        self.displays = 0
        self.max_res = 0, 0
        self._off_set_x = 0
        self._off_set_y = 0
        self.saved = False

        # Frames.  # fazer um frame base para os outros quatro frames.
        self.accounting = Accounting(self, customer=self.customer)
        self.toolbar = Toolbar(self, customer=self.customer)
        self.profile = Profile(self, customer=self.customer)
        self.status_bar = StatusBar(self)

        self.title("Constancy")

        # Binds.
        self.bind("<Map>", self.mapped)
        self.bind("<Escape>", self.f_quit)

        # Packing.
        self.toolbar.grid(row=0, column=0)
        self.accounting.grid(row=0, column=1, sticky="nsew")
        # self.profile.grid(row=0, column=1, sticky="nsew")
        self.status_bar.grid(row=1, column=0, columnspan=2)

    def show_profile(self):
        if self.frame_on_top == "profile":
            print('profile opend')
            self.profile.grid_forget()
            self.accounting.grid(row=0, column=1, sticky="nsew")
            self.accounting.tkraise()
            self.frame_on_top = "accounting"
        elif self.frame_on_top == "accounting":
            print('acc opend')
            self.accounting.grid_forget()
            self.profile.grid(row=0, column=1, sticky="nsew")
            self.profile.tkraise()
            self.frame_on_top = "profile"

    def mapped(self, event):
        self.window_status = self.window_status
        return event

    def f_quit(self, event=None):
        if self.saved:
            # deseja salvar mudanças antes de sair?
            self.destroy()
            self.master.destroy()
        else:
            # self.master.destroy()
            self.destroy()
            self.master.destroy()
        return event


def main():
    pass


if __name__ == "__main__":
    main()
