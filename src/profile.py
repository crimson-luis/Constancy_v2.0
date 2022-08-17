# from processing.database import Item, SubItem
import datetime

from processing.log_handler import Logger
# from datetime import datetime, time
from calendar import monthrange
from tkcalendar import DateEntry
from tkinter import *
import pandas as pd
from processing.database import (
    # delete_item,
    # create_item,
    # create_sub_item,
    read_items,
)
from common import (
    _entry,
    _label,
    _button,
    M_COLOR,
    M_FONT
)

# TODO:
#       - deletar perfil;
#       - botao editar;
#       - forecast;
#       - mais info;
#       - comparar;


class Profile(Frame):
    def __init__(self, master, customer):
        Frame.__init__(self, master)
        self.master = master
        self.customer = customer
        self.logger = Logger()
        self["bg"] = M_COLOR["cbg"]
        self.pack_propagate(False)
        self["width"] = 610
        self["height"] = 264
        self.items = pd.DataFrame()
        self.filtered_items = pd.DataFrame()
        self.today = datetime.datetime.today()
        self.end_of_month = monthrange(year=self.today.year, month=self.today.month)[1]

        # Functions.
        self.update_item_list()
        self.user_created_at = self.items.index.min()
        self.change_date_range(self.user_created_at, self.items.index.max())
        self.first_date = self.filtered_items.index.min()
        self.last_date = self.filtered_items.index.max()

        # Statistics.
        self.items_count = None
        self.total_spend = None
        self.total_profit = None
        self.total_balance = None
        self.average_daily_balance = None

        # Frames.
        self.info_frame = Frame(self, bg=M_COLOR["cbg"])
        self.info_frame.pack(fill=BOTH)

        # Labels.
        self.name_label = _label(
            frame=self.info_frame,
            text=f"{self.customer.id}. {self.customer.name}",
        )
        self.total_spend_label = _label(
            frame=self.info_frame,
            text=f"Gasto total: R$ ",
        )
        self.total_balance_label = _label(
            frame=self.info_frame,
            text=f"Saldo total: R$ ",
        )
        self.total_profit_label = _label(
            frame=self.info_frame,
            text=f"Lucro total: R$ ",
        )
        self.daily_balance_label = _label(
            frame=self.info_frame,
            text=f"Saldo médio por dia: R$ ",
        )
        self.total_items_label = _label(
            frame=self.info_frame,
            text=f"Total de itens: ",
        )
        self.forecast_balance_label = _label(
            frame=self.info_frame,
            text="Saldo projetado: R$ ",
        )
        self.banks_label = _label(
            frame=self.info_frame,
            text="Bancos: ",
        )
        self.user_date_label = _label(
            frame=self.info_frame,
            text=f"Usuário criado em {self.user_created_at.strftime('%d/%m/%Y')}"
        )
        self.message_lb = _label(frame=self.info_frame, text="")

        # Entries.
        self.start_date_entry = DateEntry(
            self.info_frame,
            width=8,
            font=M_FONT,
            mindate=self.first_date,
            maxdate=self.last_date,
            # date_pattern="dd/mm/yy",
            # style="EntryStyle.TEntry",
        )
        self.start_date_entry["borderwidth"] = 1
        self.start_date_entry["background"] = M_COLOR["darker"]
        self.start_date_entry["foreground"] = M_COLOR["txt"]
        self.start_date_entry.set_date(self.first_date)
        self.end_date_entry = DateEntry(
            self.info_frame,
            width=8,
            font=M_FONT,
            mindate=self.first_date,
            maxdate=self.last_date,
            # date_pattern="dd/mm/yy",
            # style="EntryStyle.TEntry",
        )
        self.end_date_entry["borderwidth"] = 1
        self.end_date_entry["background"] = M_COLOR["darker"]
        self.end_date_entry["foreground"] = M_COLOR["txt"]

        # Buttons.
        self.set_date_button = _button(frame=self.info_frame, text="Aplicar")
        self.today_button = _button(frame=self.info_frame, text="Hoje")
        self.month_button = _button(frame=self.info_frame, text="Mês Atual")
        self.compare_button = _button(frame=self.info_frame, text="Comparar")
        self.delete_item_button = _button(frame=self.info_frame, text="Exc5luir")
        self.edit_item_button = _button(frame=self.info_frame, text="Edi5tar")

        # Commands.

        # Griding.
        self.name_label.grid(row=0, column=0, sticky=W, padx=2)
        self.today_button.grid(row=0, column=1, sticky=E, padx=2, pady=2)
        self.month_button.grid(row=0, column=2, padx=2, pady=2)
        self.compare_button.grid(row=0, column=3, padx=2, pady=2)
        self.start_date_entry.grid(row=1, column=1, padx=2)
        self.end_date_entry.grid(row=1, column=2, padx=2)
        self.set_date_button.grid(row=1, column=3, sticky=E, padx=2)
        self.total_profit_label.grid(row=2, column=0, sticky=W, padx=2)
        self.total_spend_label.grid(row=3, column=0, sticky=W, padx=2)
        self.total_balance_label.grid(row=4, column=0, sticky=W, padx=2)
        self.daily_balance_label.grid(row=5, column=0, sticky=W, padx=2)
        self.total_items_label.grid(row=6, column=0, sticky=W, padx=2)
        self.forecast_balance_label.grid(row=7, column=0, sticky=W, padx=2)
        self.banks_label.grid(row=8, column=0, sticky=W, padx=2)
        self.user_date_label.grid(row=9, column=4, sticky=W, padx=2)

        # Binds.
        # self.change_date_range(start=, end=)
        self.set_date_button["command"] = self.apply_date
        self.today_button["command"] = lambda: self.set_date(
            start=self.today,
            end=self.today,
        )
        self.month_button["command"] = lambda: self.set_date(
            start=self.today.replace(day=1),
            end=self.today.replace(day=self.end_of_month),
        )

        # Calls.
        self.update_info()

    def apply_date(self):
        self.change_date_range(
            start=self.start_date_entry.get_date().strftime("%Y-%m-%d"),
            end=self.end_date_entry.get_date().strftime("%Y-%m-%d"),
        )
        self.update_info()

    def set_date(self, start, end):
        if self.validate_date(start, end):
            self.start_date_entry.set_date(date=start)
            self.end_date_entry.set_date(date=end)
            self.apply_date()

    def validate_date(self, start, end):
        if start > self.last_date or end < self.first_date:
            self.master.status_bar.show_message(text="Nenhuma informação encontrada.")
            return False
        else:
            return True

    def change_date_range(self, start, end):
        self.filtered_items = self.items.loc[start:end]
        self.filtered_items = self.filtered_items.drop(
            self.filtered_items[self.filtered_items.kind == "Base"].index
        )

    def update_item_list(self):
        self.items = pd.DataFrame(
            [vars(field) for field in read_items(customer_id=self.customer.id)]
        )
        self.items["date"] = pd.to_datetime(self.items.date)
        self.items.set_index("date", inplace=True)

    def calculate_statistics(self):
        self.average_daily_balance = self.filtered_items.value.mean()
        self.total_profit = self.filtered_items[
                               self.filtered_items.type == 1
                           ].value.sum()
        self.total_spend = self.filtered_items[
                               self.filtered_items.type == -1
                           ].value.sum()
        self.total_balance = self.total_profit + self.total_spend
        self.items_count = self.filtered_items.shape[0]
        self.last_date = self.filtered_items.index.max()

    def update_info(self):
        self.calculate_statistics()
        self.total_spend_label.configure(
            text=f"Gasto total: R$ {self.total_spend:.02f}"
        )
        self.total_profit_label.configure(
            text=f"Lucro total: R$ {self.total_profit:.02f}"
        )
        self.total_balance_label.configure(
            text=f"Saldo total: R$ {self.total_balance:.02f}"
        )
        self.daily_balance_label.configure(
            text=f"Saldo médio por dia: R$ {self.average_daily_balance:.02f}"
        )
        self.total_items_label.configure(
            text=f"Total de itens: {self.items_count}"
        )
