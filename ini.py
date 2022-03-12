# error description:
# erro 121 - senha ou usuario incorreto.
# erro 33 - valor ou descrição não definidos.
# erro 157 - erro de criacao de usuario (senha/usuario)
# erro 12 - erro na recuperacao do email

# hotkeys:
# f1 - enter with debit.
# f2 - enter with credit.
# enter create item.
# esc - reset entries.

# annotations:
# send email with html content (constancy image, etc...)
# make log list a dict (action: time)
# add "lucro total mensal" to statistcs frame
# work on inheritance (cleaner code)
# make file with user preferences (remember username...)
# see password button
# https://stackoverflow.com/questions/28795859/how-can-i-play-a-sound-when-a-tkinter-button-is-pushed
# users functionalities (delete/create user, reset balance, pwd...)
# .

# Packages.
# from cryptography.fernet import Fernet
# from tkcalendar import DateEntry
# import matplotlib.pyplot as plt
# from PIL import Image, ImageTk
# from tkinter import messagebox
# from bs4 import BeautifulSoup
# import datetime as dt
# import smtplib, ssl
# import pandas as pd
# import mplcyberpunk
# import calendar
# import main
# import json
# import ast
# import PIL
# import os

from win32api import GetSystemMetrics
from processing.database import Customer
from tkinter import ttk
from tkinter import *
from common import (
    M_FONT,
    M_COLOR,
    EMAIL_REGEX,
    resource_path,
    f_invoker,
    set_appwindow,
    change_key,
    del_win,
)
import regex as re
from threading import Thread
from string import digits
from processing import log_handler as lh, json_handler as jh, database as db
from random import choices
from src.messages import MessageWindow
from src.main import MainWindow
from src import mail


# Login/Create frame.
class LoginFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self["bg"] = M_COLOR["cbg"]
        self.place(x=41, y=200)  # margin: 41 px.
        self.grid_rowconfigure([0, 1, 2, 3, 4, 6, 7, 8], minsize=26)
        self.grid_rowconfigure(5, minsize=44)
        self.val_command = (self.register(self.f_val_entry), "%S")
        self.master = master
        self.logger = lh.Logger()

        # Labels.
        self.r_password_lb = self._label("Confirme a senha:")

        self.email_lb = self._label("Email:")

        self.user_lb = self._label("Nome de usuário: ")
        self.user_lb.grid(sticky=W)

        self.password_lb = self._label("Senha: ")
        self.password_lb.grid(row=2, sticky=W)

        self.info_lb = self._label("")
        self.info_lb.grid(row=9, columnspan=2)

        self.info_img = PhotoImage(file=resource_path("images/info2.png"))
        self.info_pw_img_lb = Label(self, width=24, height=22)
        self.info_pw_img_lb["image"] = self.info_img
        self.info_pw_img_lb["bg"] = M_COLOR["cbg"]

        # Entries.
        self.user_entry = self._entry()
        self.user_entry.config(validate="key", validatecommand=self.val_command)
        self.user_entry.grid(row=1, columnspan=2, sticky=W)
        self.user_entry.focus_force()

        self.password_entry = self._entry(show="*")
        self.password_entry.grid(row=3, sticky=W)

        self.r_password_entry = self._entry(show="*")

        self.email_entry = self._entry()

        # Buttons.
        self.create_frame_bt = self._button(w=8, h=2, text="Criar conta")
        self.create_frame_bt["command"] = self.create_frame_raise
        self.create_frame_bt.grid(row=5, sticky=W)

        self.forgot_pw_bt = self._button(w=14, h=1, text="Esqueceu a senha?")
        self.forgot_pw_bt["command"] = self.reset_frame_raise
        self.forgot_pw_bt.grid(row=4, sticky=W)

        self.login_bt = self._button(w=6, h=1, text="Próximo")
        self.login_bt["command"] = self.login_call
        self.login_bt.grid(row=5, sticky=E)

        self.view_pass_img_off = PhotoImage(
            file=resource_path("images/eye_off.png")
        )  # pyimage2
        self.view_pass_img_on = PhotoImage(
            file=resource_path("images/eye_on.png")
        )  # pyimage3
        self.view_pass_bt = self._button(w=24, h=24, text="")
        self.view_pass_bt["command"] = self.view_pass_toggle
        self.view_pass_bt["image"] = self.view_pass_img_off

        self.reset_email_img = PhotoImage(file=resource_path("images/mail.png"))
        self.send_email_bt = self._button(w=24, h=24, text="")
        self.send_email_bt["command"] = self.f_send_email
        self.send_email_bt["image"] = self.reset_email_img

        self.create_img = PhotoImage(file=resource_path("images/plus.png"))
        self.create_bt = self._button(w=24, h=24, text="")
        self.create_bt["command"] = self.f_create
        self.create_bt["image"] = self.create_img

        # Binds.
        self.email_entry.bind("<FocusOut>", lambda k: self.email_entry.xview(0))
        self.user_entry.bind("<FocusOut>", lambda k: self.email_entry.xview(0))
        self.info_pw_img_lb.bind("<Enter>", self.on_enter_info)
        self.info_pw_img_lb.bind("<Leave>", self.on_leave_info)
        self.master.bind("<Return>", lambda k: f_invoker(button=self.login_bt))
        # self.user_entry.bind('<Alt-r>', self.create_frame_raise)
        # self.bind('<Control_L+c>', lambda k: f_invoker(button=self.back_bt))

    def login_call(self):
        # self.login_bt["command"] = ""
        # if self.user_entry.get() == "" or self.password_entry.get() == "":
        #     self.info_lb.config(text="Digite alguma coisa!", fg=M_COLOR["error"])
        #     self.after(2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))
        # elif not self.f_val_login(self.user_entry.get(), self.password_entry.get()):
        #     self.info_lb.config(text="Nome ou senha incorreto!", fg=M_COLOR["error"])
        #     self.after(2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))
        # else:
            # logged_user = jh.get_info(
            #     resource_path(f"{self.user_entry.get()}.encrypted")
            # )[0]
            self.info_lb.config(text="Validando credenciais...")
            self.after(250, lambda: self.info_lb.config(text="Marcando um dez..."))
            self.after(
                700, lambda: self.info_lb.config(text="Logado!", fg=M_COLOR["success"])
            )
            self.after(950, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))
            self.after(950, lambda: self.f_login(customer_name=self.user_entry.get()))
            self.after(955, lambda: self.user_entry.delete(0, "end"))
            self.after(955, lambda: self.password_entry.delete(0, "end"))
        # self.login_bt["command"] = self.login_call

    def f_login(self, customer_name):
        print(f"nome: {customer_name}")
        customer_login = db.get_customer(name=customer_name)[0]
        print(customer_login)
        self.master.withdraw()
        if not len(db.read_items(customer_login.id)):
            MessageWindow(master=self.master, customer=customer_login)
        else:
            MainWindow(master=self.master, customer=customer_login)

    def view_pass_toggle(self):
        if str(self.view_pass_bt["image"]) == "pyimage2":
            self.password_entry["show"] = ""
            self.r_password_entry["show"] = ""
            self.view_pass_bt["image"] = self.view_pass_img_on
        elif str(self.view_pass_bt["image"]) == "pyimage3":
            self.password_entry["show"] = "*"
            self.r_password_entry["show"] = "*"
            self.view_pass_bt["image"] = self.view_pass_img_off

    def _label(self, text):
        label = Label(
            self,
            text=text,
            fg=M_COLOR["txt"],
            bg=M_COLOR["cbg"],
            font=M_FONT,
            anchor="w",
            wraplengt=146,
        )
        return label

    def _entry(self, show=""):
        entry = ttk.Entry(self, show=show, width=20, font=M_FONT)
        return entry

    def _button(self, w, h, text):
        button = Button(
            self,
            width=w,
            height=h,
            bd=0,
            text=text,
            activebackground=M_COLOR["cbg"],
            activeforeground=M_COLOR["txt"],
            bg=M_COLOR["cbg"],
            fg=M_COLOR["txt"],
            font=M_FONT,
        )
        return button

    def on_enter_info(self, event):
        self.info_lb.config(text="Mínimo de 6 dígitos.")
        return event

    def on_leave_info(self, event):
        self.info_lb.config(text="")
        return event

    def f_val_entry(self, key_in):
        if key_in in '/:*<>|"?\\':
            self.bell()
            self.info_lb.config(text="Caractere inválido.", fg=M_COLOR["error"])
            self.after(2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))
            return False
        else:
            return True

    def create_frame_raise(self):
        if not self.r_password_lb.winfo_ismapped():  # login > create
            self.master.bind("<Return>", lambda k: f_invoker(button=self.create_bt))
            self.user_entry.focus()
            self.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=26)
            self.grid_rowconfigure(8, minsize=44)
            self.info_pw_img_lb.grid(row=2, sticky=E)
            self.view_pass_bt.grid(row=4, sticky=E)
            self.r_password_lb.grid(row=4, sticky=W)
            self.r_password_entry.grid(row=5)
            self.email_lb.grid(row=6, sticky=W)
            self.email_entry.grid(row=7)
            self.create_bt.grid(row=8, sticky=E)
            self.create_frame_bt.grid(row=8, sticky=W)
            self.password_lb.configure(text="Senha:")
            self.create_frame_bt.configure(text="Fazer login")
            self.forgot_pw_bt.grid_forget()
            self.login_bt.grid_forget()
        else:
            self.master.bind("<Return>", lambda k: f_invoker(button=self.login_bt))
            self.user_entry.focus()  # create > login
            self.password_entry["show"] = "*"
            self.r_password_entry["show"] = "*"
            self.password_entry.delete(0, END)
            self.r_password_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.grid_rowconfigure([0, 1, 2, 3, 4, 6, 7, 8], minsize=26)
            self.grid_rowconfigure(5, minsize=44)
            for widget in [
                self.info_pw_img_lb,
                self.view_pass_bt,
                self.r_password_lb,
                self.r_password_entry,
                self.email_lb,
                self.email_entry,
                self.create_bt,
            ]:
                widget.grid_forget()
            self.password_lb.configure(text="Senha:")
            self.create_frame_bt.grid(row=5, sticky=W)
            self.create_frame_bt.configure(text="Criar conta")
            self.forgot_pw_bt.grid(row=4, sticky=W)
            self.login_bt.grid(row=5, sticky=E)

    def f_create(self):
        if (
            self.user_entry.get() == ""
            or self.password_entry.get() == ""
            or self.email_entry.get() == ""
        ):
            self.info_lb.config(text="Digite alguma coisa!", fg=M_COLOR["error"])
            self.after(2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))
        elif jh.user_exists(resource_path(f"{self.user_entry.get()}.encrypted")):
            self.info_lb.config(text="Usuário já existente.", fg=M_COLOR["error"])
            self.after(2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))
        elif len(self.password_entry.get()) < 6:  # Precisa de mais requisitos.
            self.info_lb.config(
                text="A senha não atende aos requisitos.",
                fg=M_COLOR["error"],
            )
            self.after(
                2000,
                lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]),
            )
        elif self.password_entry.get() != self.r_password_entry.get():
            self.info_lb.config(text="As senhas não coincidem.", fg=M_COLOR["error"])
            self.after(
                2000,
                lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]),
            )
        elif not re.match(EMAIL_REGEX, self.email_entry.get()):
            self.info_lb.config(text="Email inválido.", fg=M_COLOR["error"])
            self.after(2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))
        else:
            db.create_user(
                Customer(
                    name=self.user_entry.get(),
                    password=self.password_entry.get(),
                    email=self.email_entry.get(),
                )
            )
            jh.create_user(
                name=self.user_entry.get(),
                password=self.password_entry.get(),
                email=self.email_entry.get(),
                loc=resource_path(f"{self.user_entry.get()}.encrypted"),
            )
            self.logger.log_it(
                f"user.{self.user_entry.get()}",
                "info",
                "User creation successful.",
            )
            self.info_lb.config(
                text="Usuário criado com sucesso!", fg=M_COLOR["success"]
            )
            self.after(
                2000,
                lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]),
            )
            self.create_frame_raise()

    def f_val_login(self, name, password):
        loc = resource_path(f"{name}.encrypted")
        if jh.user_exists(loc):
            if password == jh.get_info(loc)[0]["user"]["password"]:
                self.logger.log_it(
                    f"auth.{name}", "info", "Login validation successful."
                )
                return True
            else:
                self.logger.log_it(
                    f"auth.{name}", "info", "Login validation failed, wrong password."
                )
        else:
            return False

    def reset_frame_raise(self):  # change to callback method
        if self.login_bt.winfo_ismapped():  # login > email
            self.master.bind("<Return>", lambda k: f_invoker(button=self.send_email_bt))
            self.grid_rowconfigure(5, minsize=26)
            self.grid_rowconfigure(4, minsize=44)
            self.password_entry.grid_forget()
            self.password_entry.delete(0, END)
            self.user_entry.grid_forget()
            self.user_entry.grid(row=1)
            self.password_lb.configure(text="Email:")
            self.email_entry.grid(row=3)
            self.send_email_bt.grid(row=4, sticky=E)
            self.forgot_pw_bt.grid(row=4, sticky=W)
            self.forgot_pw_bt.configure(text="Voltar", width=4, height=2)
            self.create_frame_bt.grid_forget()
            self.login_bt.grid_forget()
            self.user_entry.focus()
        else:
            self.master.bind("<Return>", lambda k: f_invoker(button=self.login_bt))
            self.grid_rowconfigure(5, minsize=44)
            self.grid_rowconfigure(4, minsize=26)  # email > login
            self.password_lb.grid(row=2, sticky=W)
            self.password_lb.configure(text="Senha:")
            self.email_entry.grid_forget()
            self.send_email_bt.grid_forget()
            self.password_entry.grid(row=3)
            self.forgot_pw_bt.grid(row=4)
            self.forgot_pw_bt.configure(text="Esqueceu a senha?", width=14, height=1)
            self.create_frame_bt.grid(row=5, sticky=W)
            self.login_bt.grid(row=5, sticky=E)
            self.email_entry.delete(0, END)
            self.user_entry.focus()

    def refresh(self):
        self.master.update()
        self.master.after(1000, self.refresh)

    def start(self, func):
        self.refresh()
        Thread(target=func).start()

    def f_send_email(self):
        loc = resource_path(f"{self.user_entry.get()}.encrypted")
        if self.user_entry.get() != "" and self.email_entry.get() != "":
            if jh.user_exists(loc):
                if re.search("@", self.email_entry.get()):
                    if self.email_entry.get() == jh.get_info(loc)[0]["user"]["email"]:
                        self.start(self.info_lb.config(text="Enviando..."))
                        new_pw = "".join(choices(digits, k=6))
                        try:
                            mail.send_mail(
                                user=self.user_entry.get(),
                                new_password=new_pw,
                                receiver=self.email_entry.get(),
                            )
                            self.start(
                                self.info_lb.config(
                                    text="Enviado!", fg=M_COLOR["success"]
                                )
                            )
                            updated_dic = jh.get_info(loc)[0]
                            updated_dic["user"]["password"] = new_pw
                            jh.write_file(loc, updated_dic)
                            self.logger.log_it(
                                f"mail.{self.user_entry.get()}",
                                "info",
                                "Password recovery email sent successfully.",
                            )
                        except Exception as exception:
                            self.start(
                                self.info_lb.config(text="Error!", fg=M_COLOR["error"])
                            )
                            self.logger.log_it(
                                f"mail.{self.user_entry.get()}",
                                "info",
                                f"Sending password recovery email failed; Error:{exception}",
                            )
                        self.after(
                            2000,
                            lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]),
                        )
                        self.reset_frame_raise()
                    else:
                        self.info_lb.config(
                            text="Email incorreto!", fg=M_COLOR["error"]
                        )
                        self.after(
                            2000,
                            lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]),
                        )
                else:
                    self.info_lb.config(text="Email inválido!", fg=M_COLOR["error"])
                    self.after(
                        2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"])
                    )
            else:
                self.info_lb.config(text="Usuário inexistente!", fg=M_COLOR["error"])
                self.after(
                    2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"])
                )
        else:
            self.info_lb.config(text="Digite alguma coisa!", fg=M_COLOR["error"])
            self.after(2000, lambda: self.info_lb.config(text="", fg=M_COLOR["txt"]))


# Login window.
class Login(Tk):
    def __init__(self):
        super().__init__()
        # self.master = master
        self.width = 228
        self.height = 512
        self.x, self.y = int(GetSystemMetrics(0) / 2 - self.width / 2), int(
            GetSystemMetrics(1) / 2 - self.height / 2
        )
        self.geometry(
            "{}x{}+{}+{}".format(self.width, self.height, self.x, self.y)
        )
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
