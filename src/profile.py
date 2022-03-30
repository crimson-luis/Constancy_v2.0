# import tkinter
# import tkinter.messagebox
# from datetime import datetime, time
from tkinter import ttk
from tkinter import *
import common as cm
# from processing.database import Item, SubItem
from processing.database import (
    # delete_item,
    # create_item,
    # create_sub_item,
    read_items,
)
# from tkcalendar import DateEntry
import pandas as pd
from processing.log_handler import Logger


class Profile(Frame):
    def __init__(self, master, customer):
        Frame.__init__(self, master)
        self.master = master
        self.customer = customer
        self.logger = Logger()
        self["bg"] = "gray"
        self.pack_propagate(False)
        self["width"] = 610
        self["height"] = 264
        self.items = pd.DataFrame()
        self.update_item_list()

        # Frames.
        self.info_frame = Frame(self, bg=cm.M_COLOR["cbg"])
        self.info_frame.pack(fill=BOTH)

        # Labels.
        self.name_label = self._label(
            frame=self.info_frame,
            text=f"{self.customer.id} - {self.customer.name}",
        )
        self.daily_balance = self._label(
            frame=self.info_frame,
            text=f"Saldo médio diário: R$ {self.items.value[1:].mean():.02f}",
        )
        self.total_items = self._label(
            frame=self.info_frame,
            text=f"Total de itens: {self.items[1:].shape[0]}",
        )
        # self.media_diaria = self._label(frame=self.info_frame, text="Descrição")
        self.forecast_balance = self._label(
            frame=self.info_frame,
            text="Saldo projetado: R$ 1M",
        )
        self.banks = self._label(
            frame=self.info_frame,
            text="Bancos: NU, Inter, Bradesco",
        )
        self.date_lb = self._label(
            frame=self.info_frame,
            text=f"Usuário criado em {self.items[:1].date.dt.strftime('%d/%m/%y')[0]}"
        )
        self.message_lb = self._label(frame=self.info_frame, text="")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            foreground=cm.M_COLOR["txt"],
            background=cm.M_COLOR["darker"],
            bordercolor=cm.M_COLOR["cbg"],
            troughcolor=cm.M_COLOR["cbg"],
            lightcolor=cm.M_COLOR["darker"],
            darkcolor=cm.M_COLOR["darker"],
            arrowcolor=cm.M_COLOR["txt"],
            arrowsize=16,
            gripcount=0,
        )
        style.configure(
            "EntryStyle.TEntry",
            background=cm.M_COLOR["p0"],
            # bordercolor="red",
            # relief="flat",
            # troughcolor=cm.M_COLOR["cbg"],
            # arrowcolor=cm.M_COLOR["txt"],
            # arrowsize=16,
            # gripcount=0,
        )
        style.layout(
            "EntryStyle.TEntry",
            [
                (
                    "Entry.plain.field",
                    {
                        "children": [
                            (
                                "Entry.background",
                                {
                                    "children": [
                                        (
                                            "Entry.padding",
                                            {
                                                "children": [
                                                    (
                                                        "Entry.textarea",
                                                        {"sticky": "nswe"},
                                                    )
                                                ],
                                                "sticky": "nswe",
                                            },
                                        )
                                    ],
                                    "sticky": "nswe",
                                },
                            )
                        ],
                        "border": "0",
                        "sticky": "nswe",
                    },
                )
            ],
        )

        # Entries.
        # self.class_entry = ttk.Entry(
        #     self.item_frame,
        #     width=10,
        #     font=cm.M_FONT,
        #     style="EntryStyle.TEntry",
        # )
        # self.description_entry = ttk.Entry(
        #     self.item_frame,
        #     width=24,
        #     font=cm.M_FONT,
        #     style="EntryStyle.TEntry",
        # )
        # self.value_entry = ttk.Entry(
        #     self.item_frame,
        #     width=8,
        #     font=cm.M_FONT,
        #     style="EntryStyle.TEntry",
        # )

        # Buttons.
        # self.add_item_button = self._button(frame=self.item_frame, text="Confirmar")
        # self.add_sub_item_button = self._button(frame=self.item_frame, text="Subitem")
        # self.cancel_button = self._button(frame=self.item_frame, text="Cancelar")
        self.delete_item_button = self._button(frame=self.info_frame, text="Excdasdluir")
        self.edit_item_button = self._button(frame=self.info_frame, text="Editsaar")
        # Commands.
        # self.add_item_button["command"] = self.add_items
        # self.delete_item_button["command"] = self.del_item
        # self.cancel_button["command"] = self.cancel
        # self.add_sub_item_button["command"] = self.toggle_sub_item
        # self.sub_toggle_button['command'] =

        # Griding.
        self.name_label.grid(row=0, column=0, sticky=W, padx=2)
        # self.class_entry.grid(row=1, column=0, padx=2)
        self.daily_balance.grid(row=1, column=0, sticky=W, padx=2)
        # self.description_entry.grid(row=1, column=1, padx=2)
        # self.sub_description_entry.grid(row=2, column=1, padx=2)
        # self.value_entry.grid(row=1, column=2, padx=2)
        # self.sub_value_entry.grid(row=2, column=2, padx=2)
        self.banks.grid(row=0, column=3, sticky=W, padx=2)
        # self.type_list.grid(row=1, column=3, sticky=W, padx=2)
        # self.add_sub_item_button.grid(row=2, column=0, padx=2)
        self.date_lb.grid(row=4, column=4, sticky=W, padx=2)
        self.total_items.grid(row=2, column=0, sticky=W, padx=2)
        self.forecast_balance.grid(row=3, column=0, sticky=W, padx=2)
        # self.date_entry.grid(row=1, column=4, padx=2)
        # self.add_item_button.grid(row=1, column=5, padx=2)
        # self.cancel_button.grid(row=2, column=5, padx=2)

    def update_item_list(self):
        self.items = pd.DataFrame(
            [vars(field) for field in read_items(customer_id=self.customer.id)]
        )

    def _label(self, frame, text, font=cm.M_FONT, anchor="w"):
        label = Label(
            frame,
            text=text,
            fg=cm.M_COLOR["txt"],
            bg=cm.M_COLOR["cbg"],
            font=font,
            anchor=anchor,
        )
        return label

    def _button(self, frame, text, font=cm.M_FONT):
        button = Button(
            frame,
            font=font,
            bg=cm.M_COLOR["darker"],
            width=8,
            height=1,
            fg=cm.M_COLOR["txt"],
            bd=0,
            text=text,
            activebackground=cm.M_COLOR["darker"],
            activeforeground=cm.M_COLOR["cbg"],
        )
        return button
