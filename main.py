from win32api import GetSystemMetrics
from tkinter import *
import pandas as pd
from PIL import ImageTk, Image
from common import M_FONT, M_COLOR, resource_path, del_win
from log_handler import Logger
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import f_graph
from accounting import Accounting
from database import read_items

# from tkinter import messagebox


class Toolbar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master  # caso nao for usar tire
        self.toolbar_frame = self
        self.toolbar_frame["bg"] = M_COLOR["darker"]
        self.items = pd.DataFrame()
        self.balance = 0
        self.showing = False
        # Images.
        self.profile_img = PhotoImage(file=resource_path("images/profile.png"))
        self.refresh_img = PhotoImage(file=resource_path("images/refresh.png"))
        self.blur_img = PhotoImage(file=resource_path("images/blur.png"))
        # Canvas.
        self.graph_preview = FigureCanvasTkAgg(
            f_graph(show=False), master=self.toolbar_frame
        )
        # self.graph_preview.draw()
        self.toolbar_canvas = Canvas(
            self.toolbar_frame,
            bg=M_COLOR["darker"],
            width=152,
            height=164,
            highlightthickness=0,
        )
        self.balance_text_lb = self.toolbar_canvas.create_text(
            8,
            8,
            text="Saldo disponível",
            anchor=NW,
            font="Roboto 8",
            fill=M_COLOR["txt"],
            tag="balance",
        )
        self.balance_value_lb = self.toolbar_canvas.create_text(
            8, 24, text="R$", anchor=NW, font=M_FONT, fill=M_COLOR["txt"], tag="balance"
        )
        self.updated_lb = self.toolbar_canvas.create_text(
            8,
            42,
            text="",
            anchor=NW,
            font="Roboto 8",
            fill=M_COLOR["txt"],
            tag="balance",
        )
        self.blur = self.toolbar_canvas.create_image(
            28, 25, image=self.blur_img, anchor=NW
        )
        # Buttons.
        self.refresh_bt = Button(
            self.toolbar_canvas,
            width=16,
            height=16,
            bd=0,
            pady=0,
            text="",
            bg=M_COLOR["darker"],
            activebackground=M_COLOR["darker"],
            image=self.refresh_img,
            command=self.refresh,
        )
        self.profile_bt = Button(
            self.toolbar_canvas,
            width=24,
            height=24,
            bd=0,
            pady=0,
            text="",
            bg=M_COLOR["darker"],
            activebackground=M_COLOR["darker"],
            image=self.profile_img,
        )
        # Placing and packing.
        self.toolbar_canvas.pack()
        self.graph_preview.get_tk_widget().pack(fill=BOTH)
        self.refresh_bt.place(x=135, y=0)
        self.profile_bt.place(x=4, y=60)
        # Binds.
        self.toolbar_canvas.tag_bind(
            self.balance_value_lb,
            "<ButtonPress-1>",
            self.view_balance_toggle
        )
        self.toolbar_canvas.tag_bind(
            self.blur,
            "<ButtonPress-1>",
            self.view_balance_toggle
        )

    def refresh(self):
        # self.graph_preview.get_tk_widget().pack(fill=BOTH)
        try:
            self.items = pd.DataFrame.from_dict([k.dict() for k in read_items()])
            self.balance = self.items.value.sum()
            self.toolbar_canvas.itemconfig(self.updated_lb, text="...")
            self.after(
                100,
                lambda: self.toolbar_canvas.itemconfig(
                    self.updated_lb, text="Atualizado"
                ),
            )
            self.after(
                900,
                lambda: self.toolbar_canvas.itemconfig(
                    self.updated_lb, text=""
                ),
            )
        except Exception as e:
            self.toolbar_canvas.itemconfig(self.updated_lb, text="...")
            self.after(
                100,
                lambda: self.toolbar_canvas.itemconfig(
                    self.updated_lb, text=f"Erro: {e}"
                ),
            )
            self.after(
                1200,
                lambda: self.toolbar_canvas.itemconfig(
                    self.updated_lb, text=""
                ),
            )

    def view_balance_toggle(self, event=None):
        if self.showing:  # unseen>seen
            self.toolbar_canvas.itemconfig(self.blur, state=NORMAL)
        else:
            self.refresh()
            self.toolbar_canvas.itemconfig(
                self.balance_value_lb, text=f"R$ {self.balance:.2f}"
            )
            self.after(
                300, lambda: self.toolbar_canvas.itemconfig(self.blur, state=HIDDEN)
            )
        self.showing = not self.showing
        return event


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self["bg"] = M_COLOR["darker"]
        # self.pack_propagate(False)
        self["height"] = 20
        self.status_bar_frame = self
        name = "Luis"

        # Labels.
        self.status_lb = Label(
            self,
            text=f"Olá, {name} - Constancy",
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
class MainWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.res_w, self.res_h = 764, 286  # carregar do arquivo de usuarios
        self.x, self.y = int(GetSystemMetrics(0) / 2 - self.res_w / 2), int(
            GetSystemMetrics(1) / 2 - self.res_h / 2
        )
        master.geometry(f"{self.res_w}x{self.res_h}+{self.x}+{self.y}")
        master.iconbitmap(resource_path("images/icon.ico"))
        master.focus_force()
        # master.resizable(0, 0)

        Logger().log_it("kern", "info", "Main window opened.")

        # Variables.
        # self.res_before = self.res_w, self.res_h
        self.loc_before = self.master.winfo_x(), self.master.winfo_y()
        self.window_status = "normal"
        self.displays = 0
        self.max_res = 0, 0
        self._off_set_x = 0
        self._off_set_y = 0
        self.saved = False

        # Frames.  # fazer um frame base para os outros quatro frames.
        self.middle_frame = Frame(master, height=492, bg="white")
        self.toolbar = Toolbar(self.middle_frame)
        self.accounting = Accounting(self.middle_frame)
        self.status_bar = StatusBar(master)

        master.title("Constancy")

        # Binds.
        master.bind("<Map>", self.mapped)
        master.bind("<Escape>", self.f_quit)

        # Packing.
        self.middle_frame.pack(fill=X)
        self.toolbar.pack(side=LEFT)
        self.accounting.pack(fill=BOTH)
        self.status_bar.pack(fill=X)

    def mapped(self, event):
        self.window_status = self.window_status
        return event

    def f_quit(self, event=None):
        if self.saved:
            # deseja salvar mudanças antes de sair?
            self.master.destroy()
        else:
            self.master.destroy()
        return event


def login():
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: del_win(root))
    root_window = MainWindow(root)
    root.mainloop()
    return root_window


if __name__ == "__main__":
    login()
