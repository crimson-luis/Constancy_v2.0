from win32api import GetSystemMetrics
from tkinter import *
import common as cm
import log_handler as lh
from tkinter import ttk
import ctypes
import accounting as ac
# from tkinter import messagebox
# from tkcalendar import DateEntry


class Toolbar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master  # caso nao for usar tire
        self.toolbar_frame = self
        self.toolbar_frame['bg'] = cm.M_COLOR['darker']

        # Images.
        self.toolbar_bg_img = PhotoImage(file=cm.resource_path('images/toolbar.png'))
        self.profile_img = PhotoImage(file=cm.resource_path('images/profile.png'))
        self.eye_img = PhotoImage(file=cm.resource_path('images/eye.png'))
        self.eye_slash_img = PhotoImage(file=cm.resource_path('images/eyeslash.png'))
        self.blur_img = PhotoImage(file=cm.resource_path('images/blur.png'))

        # Canvas.
        self.toolbar_canvas = Canvas(self.toolbar_frame, bg=cm.M_COLOR['darker'],
                                     width=152, height=492, highlightthickness=0)
        # self.toolbar = self.toolbar_canvas.create_image(0, 0, image=self.toolbar_bg_img, anchor=NW)
        self.blur = self.toolbar_canvas.create_image(28, 25, image=self.blur_img, anchor=NW)
        self.balance_text_lb = self.toolbar_canvas.create_text(
            8, 8, text='Saldo disponível', anchor=NW,
            font='Roboto 8', fill=cm.M_COLOR['txt'], tag='balance')
        self.balance_value_lb = self.toolbar_canvas.create_text(
            8, 24, text='R$', anchor=NW,
            font=cm.M_FONT, fill=cm.M_COLOR['txt'], tag='balance')
        self.updated_lb = self.toolbar_canvas.create_text(
            8, 42, text='', anchor=NW,
            font='Roboto 8', fill=cm.M_COLOR['txt'], tag='balance')

        # Buttons.
        self.eye_bt = Button(
            self.toolbar_canvas, width=24, height=20, bd=0, pady=0, text='',
            bg=cm.M_COLOR['darker'], activebackground=cm.M_COLOR['darker'],
            image=self.eye_img, command=self.view_balance_toggle)
        self.profile_bt = Button(
            self.toolbar_canvas, width=24, height=24, bd=0, pady=0, text='',
            bg=cm.M_COLOR['darker'], activebackground=cm.M_COLOR['darker'],
            image=self.profile_img)

        # Placing and packing.
        self.toolbar_canvas.pack(side=LEFT, fill=Y)
        self.eye_bt.place(x=115, y=20)
        self.profile_bt.place(x=4, y=60)

    def view_balance_toggle(self):
        if str(self.eye_bt['image']) == 'pyimage10':  # unseen>seen
            balance = '500347,83'
            self.toolbar_canvas.itemconfig(self.balance_value_lb, text=f'R$ {balance}')
            # carregando ... > after 250 ms > atualizado...
            self.toolbar_canvas.itemconfig(self.updated_lb, text='Atualizado neste momento')  # run update balance func
            self.toolbar_canvas.itemconfig(self.blur, state=HIDDEN)
            self.eye_bt['image'] = self.eye_slash_img
        elif str(self.eye_bt['image']) == 'pyimage11':
            self.toolbar_canvas.itemconfig(self.balance_value_lb, text='R$')
            self.toolbar_canvas.itemconfig(self.updated_lb, text='')
            self.toolbar_canvas.itemconfig(self.blur, state=NORMAL)
            self.eye_bt['image'] = self.eye_img


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self['bg'] = cm.M_COLOR['darker']
        # self.pack_propagate(False)
        self['height'] = 20
        self.status_bar_frame = self
        name = 'Luis'

        # Labels.
        self.status_lb = Label(
            self, text=f'Olá, {name} - Constancy', bg=cm.M_COLOR['darker'],
            fg=cm.M_COLOR['txt'], font=cm.M_FONT)
        self.status_lb.pack(side=LEFT, padx=4)
        self.version_lb = Label(
            self, text='2.0 (WIP)', bg=cm.M_COLOR['darker'],
            fg=cm.M_COLOR['txt'], font=cm.M_FONT)
        self.version_lb.pack(side=RIGHT, padx=4)

        # master.title()
        self.status_lb.configure(text='Iniciado')


# MainWindow window.
class MainWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.x, self.y = int(GetSystemMetrics(0)/2 - 480), int(GetSystemMetrics(1)/2 - 270)
        self.res_w, self.res_h = 960, 514  # carregar do arquivo de usuarios
        master.geometry(f'{self.res_w}x{self.res_h}+{self.x}+{self.y}')
        master.iconbitmap(cm.resource_path('images/icon.ico'))
        master.focus_force()
        # master.resizable(0, 0)

        lh.Logger().log_it('kern', 'info', 'Main window opened.')

        # Variables.
        # self.res_before = self.res_w, self.res_h
        self.loc_before = self.master.winfo_x(), self.master.winfo_y()
        self.window_status = 'normal'
        self.displays = 0
        self.max_res = 0, 0
        self._off_set_x = 0
        self._off_set_y = 0
        self.saved = False

        # Frames.  # fazer um frame base para os outros quatro frames.
        self.middle_frame = Frame(master, height=492, bg='white')
        self.toolbar = Toolbar(self.middle_frame)
        self.accounting = ac.Accounting(self.middle_frame)
        self.status_bar = StatusBar(master)

        master.title('Constancy')

        # Binds.
        master.bind('<Map>', self.mapped)
        master.bind('<Escape>', self.f_quit)

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
            self.quit()
        else:
            self.quit()
        return event


def login():
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', lambda: cm.del_win(root))
    root_window = MainWindow(root)
    root.mainloop()
    return root_window


if __name__ == '__main__':
    login()
