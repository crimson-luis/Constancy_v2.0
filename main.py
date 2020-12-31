import tkinter as tk
from tkinter import *
import common as cm
import log_handler as lh
from win32api import GetSystemMetrics
# from tkinter import messagebox
# from tkinter import ttk
# from tkcalendar import DateEntry


class SpyTL(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.master = master
        self.iconbitmap(cm.resource_path('images/icon.ico'))
        self.protocol('WM_DELETE_WINDOW', master.destroy)
        # self.geometry('440x400+250+250')
        self.geometry('0x0+1000000+1000000')
        self.attributes('-alpha', 0)
        self.bind('<Map>', self.min_toggle)
        self.bind('<FocusIn>', lambda x: self.master.tkraise())
        self.bind('<Unmap>', self.min_toggle)
        self.bg_img = PhotoImage(file=cm.resource_path('images/toplevel_bg.png'))
        self.label = Label(self, image=self.bg_img)
        self.label.pack()
        self.update()

    def min_toggle(self, event):
        if event.type == EventType.Map:
            self.master.deiconify()
        else:
            self.master.withdraw()


class Toolbar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        # self.toolbar_frame = Toolbar(master)
        self.toolbar_frame = Frame(master)
        self.toolbar_frame['bg'] = cm.M_COLOR['darker']
        # self.toolbar_frame.place(x=24, y=24)
        # self.toolbar_frame.pack()

        # Images.
        self.toolbar_bg_img = PhotoImage(file=cm.resource_path('images/toolbar.png'))
        self.toolbar_canvas = Canvas(self.toolbar_frame, bg=cm.M_COLOR['cbg'],
                                     width=960, height=100, highlightthickness=0)
        self.toolbar_canvas.pack(side=BOTTOM, fill=X)
        self.toolbar_canvas.create_image(960, 100, image=self.toolbar_bg_img, anchor=SE)

        # Labels.
        # self.main_lb =
        self.balance_lb = Label(self.toolbar_canvas, text='Saldo: R$XXXXXX,XX', fg=cm.M_COLOR['txt'],
                                bg=cm.M_COLOR['darker'],
                                font=cm.M_FONT, anchor='w')
        # self.balance_lb.pack()
        self.balance_lb.place(x=0, y=24)


# MainWindow window.
class MainWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.x, self.y = int(GetSystemMetrics(0)/2 - 480), int(GetSystemMetrics(1)/2 - 270)
        self.res_w, self.res_h = 960, 540
        master.geometry(f'{self.res_w}x{self.res_h}+{self.x}+{self.y}')
        master.iconbitmap(cm.resource_path('images/icon.ico'))
        # master.attributes('-topmost', 1)
        master.overrideredirect(1)
        master.resizable(0, 0)
        master['bg'] = cm.M_COLOR['cbg']
        master.title('')
        lh.Logger().log_it('kern', 'info', 'Main window opened.')

        # Variables.
        self.after(300, self.give_spy_info)
        self.spy = SpyTL(master)
        self.max_res = 0, 0
        self.res_before = self.res_w, self.res_h
        self.loc_before = self.master.winfo_x(), self.master.winfo_y()
        self.window_status = 'normal'
        self.saved = False
        self.toolbar = Toolbar(self.master).toolbar_frame
        self._off_set_x = 0
        self._off_set_y = 0

        # Frames.
        self.title_bar_frame = Frame(master, height=24, bg=cm.M_COLOR['darker'])
        self.title_bar_frame.pack(fill=X)
        self.toolbar.pack(fill=X)

        # Images.
        self.x_img = PhotoImage(file=cm.resource_path('images/x.png'))
        self.max_img = PhotoImage(file=cm.resource_path('images/max.png'))
        self.min_img = PhotoImage(file=cm.resource_path('images/min2.png'))
        self.icon_img = PhotoImage(file=cm.resource_path('images/icon.png'))

        # Labels.
        self.icon_img_lb = Label(self.title_bar_frame, width=24, height=24,  # button
                                 image=self.icon_img, bg=cm.M_COLOR['darker'])
        self.icon_img_lb.pack(side=LEFT)

        # name = cm.logged_user['user']['name']
        name = 'Luis'
        self.title_label = Label(self.title_bar_frame,
                                 text=f'{name} - Constancy 2.0',
                                 fg=cm.M_COLOR['txt'], font=cm.M_FONT,
                                 bg=cm.M_COLOR['darker'])
        self.title_label.pack(side=LEFT)

        # Buttons.
        self.quit_bt = self._button(command=self.f_quit, image=self.x_img)

        self.max_bt = self._button(command='', image=self.max_img)

        self.min_bt = self._button(command=self.minimize_function, image=self.min_img)

        # Binds.
        self.max_bt.bind('<Button-1>', self.max_toggle)
        self.title_bar_frame.bind('<Button-1>', self.click_win)
        self.title_bar_frame.bind('<Map>', self.mapped)
        # self.title_bar_frame.bind('<B1-Motion>', self.drag_win)  # <ButtonRelease-1>
        # self.title_bar_frame.bind('<B1-Motion>', self.drag_2)
        # self.title_bar_frame.bind('<FocusOut>', lambda: print('ok'))
        self.title_bar_frame.bind('<Double-Button-1>', lambda k: cm.f_invoker(self.max_bt))
        master.bind('<Escape>', self.f_quit)

    def _button(self, command, image):
        button = Button(
            self.title_bar_frame, width=24, height=24, bd=0, text='',
            pady=0, activebackground=cm.M_COLOR['darker'],
            command=command, bg=cm.M_COLOR['darker'], image=image
        )
        button.pack(side=RIGHT)
        return button

    def give_spy_info(self):
        print('spy triggered')
        self.spy.state('zoomed')
        self.max_res = self.spy.winfo_width(), self.spy.winfo_height()
        self.spy.geometry('0x0+1000000+1000000')
        # print(self.spy.geometry())
        # print(useful_size_x, useful_size_y)
        # return useful_size_x, useful_size_y

    def maximize_function(self, event):
        # self.spy.state('zoomed')
        # self.max_res = self.give_spy_info()[0], self.give_spy_info()[1]
        self.window_status = 'zoomed'
        self.master.geometry(f'{self.max_res[0]}x{self.max_res[1] + 24}+0+0')
        return event

    def minimize_function(self):
        # self.window_status = 'withdrawn'
        self.spy.iconify()

    def max_toggle(self, event):
        if self.window_status == 'normal':
            self.loc_before = self.master.winfo_x(), self.master.winfo_y()
            self.maximize_function(event)
        elif self.window_status == 'zoomed':
            self.master.geometry(f'{self.res_w}x{self.res_h}'
                                 f'+{self.loc_before[0]}+{self.loc_before[1]}')
            print(f'zoomed>normal: {self.loc_before}')
            self.window_status = 'normal'

    def mapped(self, event):
        # self.window_status = 'normal'
        return event

    def border_lock(self):
        if self.master.winfo_pointery() <= 1:
            self.title_bar_frame.bind('<ButtonRelease-1>', self.maximize_function)
            self.spy.tkraise()
            self.spy.lower(belowThis=self.master)
            self.spy.attributes('-alpha', 0.2)
        else:
            # self.spy.state('withdrawn')
            self.spy.attributes('-alpha', 0)
            self.title_bar_frame.bind('<ButtonRelease-1>', '')

    def drag_left(self, event):
        self.master.state('normal')
        self.window_status = 'normal'
        self.x = self.master.winfo_pointerx() - self._off_set_x
        self.y = self.master.winfo_pointery() - self._off_set_y
        self.master.geometry(f'{self.res_w}x{self.res_h}+{self.x}+{self.y}')
        self.border_lock()
        return event

    def drag_middle(self, event):
        self.master.state('normal')
        self.window_status = 'normal'
        self.x = self.winfo_pointerx() - 480
        self.y = self.master.winfo_pointery() - self._off_set_y
        self.master.geometry(f'{self.res_w}x{self.res_h}+{self.x}+{self.y}')
        self.border_lock()
        return event

    def drag_right(self, event):
        self.master.state('normal')
        self.window_status = 'normal'
        self.x = self.winfo_pointerx() - 880
        self.y = self.master.winfo_pointery() - self._off_set_y
        self.master.geometry(f'{self.res_w}x{self.res_h}+{self.x}+{self.y}')
        self.border_lock()
        return event

    def drag_all(self, event):
        self.window_status = 'normal'
        self.x = self.master.winfo_pointerx() - self._off_set_x
        self.y = self.master.winfo_pointery() - self._off_set_y
        self.master.geometry(f'{self.res_w}x{self.res_h}+{self.x}+{self.y}')
        self.border_lock()
        return event

    def click_win(self, event):
        if self.window_status == 'zoomed':
            if self.master.winfo_pointerx() < 480:
                self.title_bar_frame.bind('<B1-Motion>', self.drag_left)
            elif self.master.winfo_pointerx() > self.max_res[0] - 480:
                self.title_bar_frame.bind('<B1-Motion>', self.drag_right)
            else:
                self.title_bar_frame.bind('<B1-Motion>', self.drag_middle)
        elif self.window_status == 'normal':
            self.title_bar_frame.bind('<B1-Motion>',  self.drag_all)
        self.loc_before = self.master.winfo_x(), self.master.winfo_y()
        self._off_set_x = event.x
        self._off_set_y = event.y

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
