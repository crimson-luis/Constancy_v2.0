from tkinter import ttk
from tkinter import *
import common as cm


class Accounting(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        # self.accounting_frame = self
        self['bg'] = 'gray'

        # Variables.
        self.bg_color = cm.M_COLOR['cbg']

        # Frames.
        self.item_frame = Frame(self, bg='black')
        self.item_frame.pack(fill=BOTH, anchor=N)
        self.info_frame = Frame(self, bg='blue')
        self.info_frame.pack()
        self.all_frame = Frame(self, bg='pink')
        self.all_frame.pack()

        # Labels.
        self.description_lb = self._label(frame=self.item_frame, text='Descrição')
        self.value_lb = self._label(frame=self.item_frame, text='Valor')
        self.date_lb = self._label(frame=self.item_frame, text='Data')
        self.sub_description_lb = self._label(frame=self.item_frame, text='Descrição do subitem')
        self.sub_value_lb = self._label(frame=self.item_frame, text='Valor do subitem')

        # Entries.
        self.description_entry = ttk.Entry(self.item_frame, width=24, font=cm.M_FONT)
        self.value_entry = ttk.Entry(self.item_frame, width=20, font=cm.M_FONT)
        self.date_entry = ttk.Entry(self.item_frame, width=12, font=cm.M_FONT)  # change to tkcalendar
        self.sub_description_entry = ttk.Entry(self.item_frame, width=24, font=cm.M_FONT)
        self.sub_value_entry = ttk.Entry(self.item_frame, width=20, font=cm.M_FONT)

        # Buttons.
        self.add_button = Button(self.item_frame, width=8, height=1, bd=0, text='Confirmar')
        self.cancel_button = Button(self.item_frame, width=8, height=1, bd=0, text='Cancelar')
        self.sub_toggle_button = Button(self.item_frame, width=2, height=1, bd=0, text='T')

        # Griding.
        self.sub_toggle_button.grid(row=1, column=0)
        self.description_lb.grid(row=0, column=1, sticky=W)
        self.value_lb.grid(row=0, column=2, sticky=W)
        self.date_lb.grid(row=0, column=3, sticky=W)
        self.description_entry.grid(row=1, column=1)
        self.value_entry.grid(row=1, column=2)
        self.date_entry.grid(row=1, column=3)
        self.sub_description_lb.grid(row=2, column=1, sticky=W)
        self.sub_value_lb.grid(row=2, column=2, sticky=W)
        self.sub_description_entry.grid(row=3, column=1)
        self.sub_value_entry.grid(row=3, column=2)
        self.add_button.grid(row=4, column=2)
        self.cancel_button.grid(row=4, column=3)

    def _label(self, frame, text, font=cm.M_FONT):
        label = Label(
            frame, text=text, fg=cm.M_COLOR['txt'],
            bg=self.bg_color, font=font,
            anchor='w')
        return label
