from win32api import GetSystemMetrics
from processing import log_handler as lh
from tkinter import ttk
import datetime
from tkinter import *
from processing.database import Item, create_item
from src.main import MainWindow
from common import (
    M_FONT,
    M_COLOR,
    set_app_window,
)


class MessageWindow(Toplevel):
    def __init__(self, master, customer):
        super().__init__()
        # self.message = message
        self.customer = customer
        self.master = master
        self.width = 280
        self.height = 112
        self.x, self.y = int(GetSystemMetrics(0) / 2 - self.width / 2), int(
            GetSystemMetrics(1) / 2 - self.height / 2
        )
        self.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))
        # master.iconbitmap(resource_path("images/icon.ico"))
        self.attributes("-topmost", 1)
        self.overrideredirect(1)
        self.resizable(0, 0)
        self["bg"] = M_COLOR["cbg"]
        self.title("")
        lh.Logger().log_it("kern", "info", "Message window opened.")
        set_app_window(self)

        # Buttons.
        self.send_bt = Button(self, width=6, height=1, bd=0, text="OK", pady=0)
        self.send_bt["activebackground"] = M_COLOR["cbg"]
        self.send_bt["activeforeground"] = M_COLOR["txt"]
        self.send_bt["foreground"] = M_COLOR["txt"]
        self.send_bt["bg"] = M_COLOR["cbg"]
        self.send_bt["command"] = self.proceed
        self.send_bt["font"] = M_FONT
        self.send_bt.place(x=208, y=80)

        self.cancel_bt = Button(self, width=6, height=1, bd=0, text="Cancelar", pady=0)
        self.cancel_bt["activebackground"] = M_COLOR["cbg"]
        self.cancel_bt["activeforeground"] = M_COLOR["txt"]
        self.cancel_bt["foreground"] = M_COLOR["txt"]
        self.cancel_bt["bg"] = M_COLOR["cbg"]
        self.cancel_bt["command"] = self.cancel
        self.cancel_bt["font"] = M_FONT
        self.cancel_bt.place(x=16, y=80)

        # Entries.
        self.main_entry = ttk.Entry(self, width=34, font=M_FONT)
        self.main_entry.insert(0, 0)
        self.main_entry.place(x=140, y=56, anchor="center")

        # Labels.
        self.main_label = Label(
            self,
            text="Informe o saldo inicial.",
            fg=M_COLOR["txt"],
            bg=M_COLOR["cbg"],
            font=M_FONT,
            # anchor="n",
            # wraplengt=146,
        )
        self.main_label.place(x=140, y=16, anchor="center")
        # self.bind("<Escape>", self.f_quit)

    def cancel(self):
        print("cancel")
        self.destroy()
        self.master.deiconify()

    def proceed(self):  # Validate if is number.
        create_item(
            Item(
                customer_id=self.customer.id,  # 1 de teste
                date=datetime.datetime.now(),
                kind="Base",
                type=1,
                description="Saldo Inicial",
                value=self.main_entry.get(),
            )
        )
        self.destroy()
        MainWindow(customer=self.customer, master=self.master)


def show():
    pass


if __name__ == "__main__":
    show()
