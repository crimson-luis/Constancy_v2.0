import tkinter
import tkinter.messagebox
from datetime import datetime, time
from tkinter import ttk
from tkinter import *
from common import _entry, _label, _button, M_COLOR, M_FONT
from processing.database import (
    Item,
    SubItem,
    sqmodel_to_df,
    delete_item,
    create_item,
    create_sub_item,
    read_items,
)
from tkcalendar import DateEntry
from processing.log_handler import Logger


# TODO:
#       - arrumar label da listbox;
#       - adicionar a possibilidade de editar item/subitem;
#       - subitems com msm nome nao sao diferenciados;
#       - adicionar filtro de items;
#       - ligar atualização de items com outros frames (profile);
#       - usar zero e um no tipo de transacao;
#       - item list distribuído e atualizado pela main;


class ItemError(Exception):
    def __init__(self, error_type, message):
        # Call the base class constructor with the parameters it needs
        self.error_type = error_type
        self.message = message

        super(ItemError, self).__init__(f"Error Type: {error_type}, Message: {message}")

    def __reduce__(self):
        return ItemError, (self.error_type, self.message)


class Accounting(Frame):
    def __init__(self, master, customer):
        Frame.__init__(self, master)
        self.bg_color = M_COLOR["cbg"]
        self.selected_item_index = None
        self.items_list = list()
        self.sub_items = dict()
        self.add_sub_item = True
        self.customer = customer
        self.logger = Logger()
        self.master = master
        self["bg"] = "gray"
        # self.query_list = list()
        # self.sub_item_list = list()

        # Frames.
        # self.left_frame = Frame(self, bg=self.bg_color)
        self.item_selection_frame = Frame(self, bg=self.bg_color)
        self.item_selection_frame.grid(row=0, column=0, sticky="nsew")
        self.insert_item_frame = InsertItem(master=self, customer=self.customer)
        self.insert_item_frame.grid(row=0, column=1, sticky="nsew")
        self.info_item_frame = ItemInfo(master=self, customer=self.customer)
        self.info_item_frame.grid(row=0, column=1, sticky="nsew")
        self.sub_item_frame = Frame(self.insert_item_frame, bg="pink")

        # Labels.
        self.message_lb = _label(frame=self.item_selection_frame, text="")
        # self.sub_description_lb = _label(frame=self.item_frame, text='Subitem')
        # self.sub_value_lb = _label(frame=self.item_frame, text='Valor do subitem')
        self.items_lb = _label(
            frame=self.item_selection_frame,
            text="Itens",
            font="Roboto 10 bold",
            anchor="center"
        )

        # Entries.
        self.search_entry = _entry(self.item_selection_frame, width=38)
        self.search_entry.insert(0, "Pesquisar...")

        # Buttons.
        self.insert_item_button = _button(frame=self.item_selection_frame, text="Inserir")
        self.edit_item_button = _button(frame=self.item_selection_frame, text="Editar")
        self.delete_item_button = _button(frame=self.item_selection_frame, text="Excluir")
        # self.graph_button = _button(frame=self.info_frame, text='Editar')

        # Others
        self.items_listbox = Listbox(
            self.item_selection_frame,
            width=40,
            bg=self.bg_color,
            font=M_FONT,
            fg=M_COLOR["txt"],
            bd=0,
            relief=FLAT,
            selectbackground=M_COLOR["darker"],
            highlightthickness=0,
            selectforeground=M_COLOR["txt"],
        )

        self.items_scrollbar = ttk.Scrollbar(self.item_selection_frame, orient=VERTICAL)
        self.items_listbox.config(yscrollcommand=self.items_scrollbar.set)
        self.items_scrollbar.config(command=self.items_listbox.yview)

        # Commands.
        self.insert_item_button["command"] = self.insert_item_frame.tkraise
        self.edit_item_button["command"] = self.info_item_frame.tkraise
        self.delete_item_button["command"] = self.del_item

        # Griding.
        self.items_lb.grid(row=0, column=0, sticky=W, padx=2)
        self.search_entry.grid(row=1, column=0, padx=2, columnspan=4)
        self.items_listbox.grid(row=2, columnspan=4, sticky=NSEW, padx=2, pady=2)
        self.items_scrollbar.grid(row=2, column=3, sticky=N + S + E, pady=4)
        self.delete_item_button.grid(row=3, column=0, padx=1)
        self.edit_item_button.grid(row=3, column=1, padx=1)
        self.insert_item_button.grid(row=3, column=2, padx=1)
        self.message_lb.grid(row=4, column=0, sticky=W, columnspan=6)
        self.get_items()
        # self.toggle_sub_item()
        # self.get_sub_items()
        for item in self.items_list:
            self.update_string(last_item=item)
        self.items_listbox.selection_set(0)
        # self.listbox.select_set(0)  # This only sets focus on the first item.
        self.listbox_callback()
        # self.items_listbox.event_generate("<<ListboxSelect>>")

        # Binds.
        # self.bind('<Control-s>', self.save)
        self.items_listbox.bind("<<ListboxSelect>>", self.listbox_callback)
        self.search_entry.bind(
            "<FocusIn>",
            lambda x: clear_entry(text="Pesquisar...", widget=self.search_entry)
        )
        self.search_entry.bind(
            "<FocusOut>",
            lambda x: set_info_text(text="Pesquisar...", widget=self.search_entry)
        )
        # self.items_listbox.bind('<FocusOut>', lambda: self.selected_item_index = 0)
        # self.bind('<Escape>', lambda k: f_invoker(button=self.cancel_button))

    # def show_profile(self):
    #     if self.frame_on_top == "profile":
    #         self.accounting.tkraise()
    #         self.frame_on_top = "accounting"
    #     elif self.frame_on_top == "accounting":
    #         self.profile.tkraise()
    #         self.frame_on_top = "profile"

    def error_label(self, text: str):
        self.message_lb.config(text=text, fg=M_COLOR["error"])
        self.after(100, lambda: self.message_lb.config(text=text, fg=M_COLOR["txt"]))
        self.after(
            200, lambda: self.message_lb.config(text=text, fg=M_COLOR["error"])
        )
        self.after(400, lambda: self.message_lb.config(text=text, fg=M_COLOR["txt"]))
        self.after(3000, lambda: self.message_lb.config(text=""))

    # def toggle_sub_item(self):
    #     self.add_sub_item = not self.add_sub_item
    #     print("add sub item?", self.add_sub_item)
    #     last_color = self.add_sub_item_button["background"]
    #     if last_color == M_COLOR["darker"]:
    #         self.sub_description_entry.grid_remove()
    #         self.sub_value_entry.grid_remove()
    #         self.sub_description_entry.delete(0, END)
    #         self.sub_value_entry.delete(0, END)
    #         self.add_sub_item_button["background"] = self.bg_color
    #     elif last_color == self.bg_color:
    #         self.sub_description_entry.grid(row=2, column=1)
    #         self.sub_value_entry.grid(row=2, column=2)
    #         self.add_sub_item_button["background"] = M_COLOR["darker"]

    def del_item(self):  # excluir subitems, proibir de excluir o Saldo Inicial
        if not self.selected_item_index or len(self.items_list) < 2:
            print("Nenhum item selecionado/Nao pode ser deletado.")
            return
        if tkinter.messagebox.askyesno(
            title="Constancy",
            message="Confirmar exclusão?",
            parent=self,
        ):
            delete_item(self.items_list.pop(self.selected_item_index).id)
            self.items_listbox.delete(self.items_listbox.curselection()[0])
            self.get_items()
            self.master.toolbar.refresh()
            self.items_listbox.selection_set(0)
            self.items_listbox.activate(0)
            self.listbox_callback()
            # self.items_listbox.see(1)
        self.master.focus()  # arrumar isso!

    def get_items(self):
        self.items_list = read_items(customer_id=self.customer.id)
        self.order_items()

    def order_items(self):
        df = (
            sqmodel_to_df(self.items_list)
            .sort_values(by=["date"])
        )
        self.items_list = [Item(
            id=row[0],
            date=row[1],
            kind=row[2],
            type=row[3],
            description=row[4],
            value=row[5],
            customer_id=row[6],
        )
            for row in zip(
                df["id"],
                df["date"],
                df["kind"],
                df["type"],
                df["description"],
                df["value"],
                df["customer_id"],
            )
        ]

    # def get_sub_items(self):  #
    #     self.items_list = read_sub_items(item_id=1)

    def update_string(self, last_item):  # adicionar data a linha
        # if self.sub_items_list
        if type(last_item) == Item:
            type_text = "Item"
        else:
            type_text = "SubItem"
        line = (
            f'{last_item.date.strftime("%d/%m/%y")} — {type_text}: {last_item.kind},'
            f" {last_item.description}"
        )
        self.items_listbox.insert(0, line)

    def listbox_callback(self, event=None):
        try:
            self.selected_item_index = (
                len(self.items_list) - 1 - self.items_listbox.curselection()[0]
            )
            self.info_item_frame.update_info(
                item=self.items_list[self.selected_item_index]
            )
            self.info_item_frame.tkraise()
            print(self.selected_item_index)
        except IndexError:
            pass


class InsertItem(Frame):
    def __init__(self, master, customer):
        Frame.__init__(self, master)
        self.bg_color = M_COLOR["cbg"]
        self.selected_item_index = None
        self.items_list = list()
        self.sub_items = dict()
        self.logger = Logger()
        self.master = master
        self.customer = customer
        self["bg"] = self.bg_color
        self.register_function = self.register(self.on_validate)

        # Labels.
        self.class_lb = _label(frame=self, text="Classe")
        self.description_lb = _label(frame=self, text="Descrição")
        self.value_lb = _label(frame=self, text="Valor")
        self.date_lb = _label(frame=self, text="Data")

        # Entries.
        # change class entry to lisbox.
        self.class_entry = _entry(self, width=10)
        self.description_entry = _entry(self, width=16)
        self.value_entry = _entry(self)
        self.value_entry.config(
            validate="key",
            validatecommand=(self.register_function, "%P")
        )
        self.date_entry = DateEntry(
            self,
            width=8,
            font=M_FONT,
            # date_pattern="dd/mm/yy",
            # style="EntryStyle.TEntry",
        )
        self.date_entry["borderwidth"] = 1
        self.date_entry["background"] = M_COLOR["darker"]
        self.date_entry["foreground"] = M_COLOR["txt"]
        self.sub_description_entry = _entry(self, width=16)
        self.sub_value_entry = _entry(self)
        self.sub_value_entry.config(
            validate="key",
            validatecommand=(self.register_function, "%P")
        )
        self.type_values = ("Gasto", "Ganho")  # assure that pos 0 is debit.
        self.type_list = ttk.Combobox(
            self,
            width=8,
            font=M_FONT,
            style="ComboBoxStyle.TCombobox",
            values=self.type_values,
            state="readonly",
        )
        self.type_list.set(self.type_values[0])
        self.subitems_listbox = Listbox(
            self,
            width=12,
            height=6,
            bg=self.bg_color,
            font=M_FONT,
            fg=M_COLOR["txt"],
            bd=0,
            relief=FLAT,
            selectbackground=M_COLOR["darker"],
            highlightthickness=0,
            selectforeground=M_COLOR["txt"],
        )
        self.subitems_scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.subitems_listbox.config(yscrollcommand=self.subitems_scrollbar.set)
        self.subitems_scrollbar.config(command=self.subitems_listbox.yview)

        # Buttons.
        self.add_item_button = _button(frame=self, text="Confirmar")
        self.add_sub_item_button = _button(frame=self, text="Subitem")
        self.cancel_button = _button(frame=self, text="Cancelar")
        self.delete_subitem_button = _button(frame=self, text="Excluir")

        # Placement.
        self.class_lb.grid(row=0, column=0, sticky=W, padx=2)
        self.description_lb.grid(row=0, column=1, sticky=W, padx=2)
        self.value_lb.grid(row=0, column=2, sticky=W, padx=2)
        self.class_entry.grid(row=1, column=0, padx=2)
        self.description_entry.grid(row=1, column=1, padx=2)
        self.value_entry.grid(row=1, column=2, padx=2)
        self.date_entry.grid(row=2, column=3, padx=2)
        self.sub_description_entry.grid(row=2, column=1, padx=2)
        self.sub_value_entry.grid(row=2, column=2, padx=2)
        self.type_list.grid(row=1, column=3, sticky=E, padx=2)
        self.sub_description_entry.grid(row=2, column=1)
        self.sub_value_entry.grid(row=2, column=2)
        self.add_sub_item_button.grid(row=2, column=0, padx=2)
        self.delete_subitem_button.grid(row=4, column=0, padx=2)
        self.cancel_button.grid(row=5, column=0, padx=2)
        self.add_item_button.grid(row=5, column=3, padx=2)
        self.subitems_listbox.grid(row=3, column=0, columnspan=4, sticky=NSEW)
        self.subitems_scrollbar.grid(row=3, column=3, sticky=N + S + E)

        # Binds.
        self.add_item_button["command"] = self.add_items
        self.cancel_button["command"] = self.cancel
        self.add_sub_item_button["command"] = self.update_sub_items
        self.bind("<Return>", self.add_items)

    def on_validate(self, p):
        # Allow blank entry
        if p == "":
            return True
        try:
            # Allow floats
            float(p)
            return True
        except ValueError:
            try:
                # Allow list of floats separated by ;
                p_list = p.split(";")
                for i in p_list:
                    float(i)
                return True
            except ValueError:
                self.master.master.bell()
                return False

    def add_items(self):
        """Add item and/or sub item list to database, considering the operation type
        (from type_list entry)."""
        # create a stringvar to represent op_type.
        operation_type = -1 if self.type_list.get() == self.type_values[0] else 1
        items = self.description_entry.get().split(";")
        values = self.value_entry.get().split(";")
        print(values, items)
        if "" in items or "" in values or self.class_entry.get() == "":
            self.master.error_label(
                text="Os campos Classe, Descrição ou Valor precisam ser preenchidos."
            )
            self.description_entry.focus()
            return
        if len(items) != len(values):
            self.master.error_label(
                text="A quantidade de items na Descrição precisa ser igual "
                "à quantidade de valores."
            )
            self.description_entry.focus()
            return
        if len(items) > 1 and (
            self.sub_description_entry.get() != "" or self.sub_value_entry.get() != ""
        ):
            self.master.error_label(
                text="Múltiplos produtos na Descrição não podem ter " "Subitems"
            )
            self.sub_description_entry.focus()
            return
        values = [float(k) for k in values]
        items_dict = dict(zip(items, values))
        # Passing every item to a Item class (sqlmodel).
        items_list = [
            Item(
                customer_id=self.customer.id,  # 1 de teste
                # Datetime combine captures date from entry and joins with 00:00
                # the plan is to have purchase time and created_at time
                # purchase time still cannot be obtained.
                date=datetime.combine(self.date_entry.get_date(), time()),
                kind=self.class_entry.get(),
                type=operation_type,
                description=i,
                value=operation_type * v,
            )
            for i, v in items_dict.items()
        ]
        try:
            self.store_sub_items(items_list)
            for item in items_list:
                create_item(item)
                self.master.get_items()
                self.logger.log_it("kern", "info", f"Commit done: {item}.")
                self.master.update_string(item)
            self.master.master.toolbar.refresh()
            self.cancel()
            self.class_entry.focus()
        except ItemError as ie:
            self.master.error_label(text=str(ie.message))

    def store_sub_items(self, items_list):
        print(self.sub_items)
        if len(items_list) > 1 or not self.sub_items:
            print(self.sub_items, "passed")
            return
        item = items_list[0]
        sub_items_list = [subitem for subitem in self.sub_items.keys()]
        sub_values_list = [value for value in self.sub_items.values()]
        if "" in sub_items_list or "" in sub_values_list:
            self.sub_description_entry.focus()
            raise ItemError(
                error_type="Subitem",
                message="Os campos Descrição ou Valor precisam ser preenchidos.",
            )
        if len(sub_items_list) != len(sub_values_list):
            self.sub_value_entry.focus()
            raise ItemError(
                error_type="Subitem",
                message="Quantidade de produtos e valores diferentes!",
            )
        sub_values_list = [float(k) for k in sub_values_list]
        # Calculate if the sum of sub items is *equal (20 cents approx.) to total value
        if abs(sum(sub_values_list) - item.type * item.value) >= 0.2:
            self.sub_value_entry.focus()
            raise ItemError(
                error_type="Subitem",
                message="Soma dos valores dos produtos diferente do valor do item!",
            )
        for index in range(len(sub_items_list)):
            print("subitemadded")
            last_sub_item = SubItem(
                item=item, description=sub_items_list[index], value=sub_values_list[index]
            )
            create_sub_item(last_sub_item)
            self.master.get_items()
            self.logger.log_it("kern", "info", f"Commit done: {last_sub_item}.")
        self.sub_items.clear()
        # limppar listbox tb

    def update_sub_items(self):
        if not (self.sub_description_entry.get() and self.sub_value_entry.get()):
            self.master.error_label(
                text="Os campos Descrição ou Valor precisam ser preenchidos."
            )
            self.sub_description_entry.focus()
            return
        self.sub_items.update(
            {self.sub_description_entry.get(): float(self.sub_value_entry.get())}
        )
        line = (
            f"{self.sub_description_entry.get()} - "
            f"R${float(self.sub_value_entry.get()):.02f}"
        )
        self.subitems_listbox.insert(0, line)
        self.sub_value_entry.delete(0, END)
        self.sub_description_entry.delete(0, END)
        self.value_entry.delete(0, END)
        self.value_entry.insert(0, sum(self.sub_items.values()))
        self.sub_description_entry.focus()

    def cancel(self):
        self.class_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.sub_description_entry.delete(0, END)
        self.value_entry.delete(0, END)
        self.sub_value_entry.delete(0, END)
        self.class_entry.focus()
        self.subitems_listbox.delete(0, END)


class ItemInfo(Frame):
    def __init__(self, master, customer):
        Frame.__init__(self, master)
        self.bg_color = M_COLOR["cbg"]
        self.selected_item_index = None
        self.customer = customer
        self.items_list = list()
        self.sub_items = dict()
        self.logger = Logger()
        self.master = master
        self["bg"] = self.bg_color

        # Labels.
        self.info_lb = _label(
            frame=self,
            text="Informações do item selecionado:",
            font="Roboto 10 bold",
        )
        self.id_lb = _label(frame=self, text="ID:")
        self.date_lb = _label(frame=self, text="Data:")
        self.kind_lb = _label(frame=self, text="Tipo:")
        self.description_lb = _label(frame=self, text="Descrição:")
        self.type_lb = _label(frame=self, text="Tipo de transação:")
        self.value_lb = _label(frame=self, text="Valor:")

        # Placement.
        self.info_lb.grid(row=0, column=0, padx=2, pady=4, sticky=W)
        self.id_lb.grid(row=1, column=0, padx=2, sticky=W)
        self.date_lb.grid(row=2, column=0, padx=2, sticky=W)
        self.kind_lb.grid(row=3, column=0, padx=2, sticky=W)
        self.description_lb.grid(row=4, column=0, padx=2, sticky=W)
        self.type_lb.grid(row=5, column=0, padx=2, sticky=W)
        self.value_lb.grid(row=6, column=0, padx=2, sticky=W)

    def update_info(self, item):
        transaction_type = "Débito" if item.type == -1 else "Crédito"
        date_text = item.date.strftime("%d/%m/%Y, %H:%M:%S")
        self.id_lb.configure(text=f"ID: {item.id}")
        self.date_lb.configure(text=f"Data: {date_text}")
        self.kind_lb.configure(text=f"Tipo: {item.kind}")
        self.description_lb.configure(text=f"Descrição: {item.description}")
        self.type_lb.configure(text=f"Tipo de transação: {transaction_type}")
        self.value_lb.configure(text=f"Valor: {item.value}")


def clear_entry(text, widget, event=None):
    if widget.get() == text:
        widget.delete(0, END)


def set_info_text(text, widget, event=None):
    if widget.get() == "":
        widget.insert(0, text)
