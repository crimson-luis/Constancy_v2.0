from datetime import datetime, time
from tkinter import ttk
from tkinter import *
import common as cm
from models import Item, SubItem, Customer
from database import (
    delete_item,
    create_item,
    create_sub_item,
    read_items,
    read_sub_items,
)
from tkcalendar import DateEntry
from log_handler import Logger


# TODO:
# fazer menu com opcoes em toolbar.
# perguntar se deseja exlcuir realmente no delete_item
# arrumar label da listbox
# arrumar data
# separar funcao de item e subitem
# botao de mostrar gráfico ampliado
# botao de adicionar subitem
# editar item/subitem


class ItemError(Exception):
    def __init__(self, error_type, message):
        # Call the base class constructor with the parameters it needs
        self.error_type = error_type
        self.message = message

        super(ItemError, self).__init__(f"Error Type: {error_type}, Message: {message}")

    def __reduce__(self):
        return ItemError, (self.error_type, self.message)


class Accounting(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        # self.accounting_frame = self
        self["bg"] = "gray"

        # Variables.
        self.bg_color = cm.M_COLOR["cbg"]
        self.customer_id = 1
        self.items_list = list()
        self.add_sub_item = True
        self.selected_item_index = 0
        # self.query_list = list()
        # self.sub_item_list = list()

        # Frames.
        self.item_frame = Frame(self, bg=self.bg_color)
        self.item_frame.pack(fill=BOTH, anchor=N)
        self.info_frame = Frame(self, bg=self.bg_color)
        self.info_frame.pack(fill=BOTH)
        self.all_frame = Frame(self, bg="pink")
        # self.all_frame.pack()

        # Labels.
        self.class_lb = self._label(frame=self.item_frame, text="Classe")
        self.description_lb = self._label(frame=self.item_frame, text="Descrição")
        self.value_lb = self._label(frame=self.item_frame, text="Valor")
        self.type_lb = self._label(frame=self.item_frame, text="Tipo")
        self.date_lb = self._label(frame=self.item_frame, text="Data")
        self.message_lb = self._label(frame=self.info_frame, text="")
        # self.sub_description_lb = self._label(frame=self.item_frame, text='Subitem')
        # self.sub_value_lb = self._label(frame=self.item_frame, text='Valor do subitem')
        self.items_listbox = Listbox(
            self.info_frame,
            width=87,
            bg=self.bg_color,
            font=cm.M_FONT,
            fg=cm.M_COLOR["txt"],
            bd=0,
            relief=FLAT,
            selectbackground=cm.M_COLOR["darker"],
            highlightthickness=0,
            selectforeground=cm.M_COLOR["txt"],
        )
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Vertical.TScrollbar",
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
        # style.configure(
        #     "ComboBoxStyle.TCombobox",
        #     background=cm.M_COLOR["darker"],
        #     foreground=cm.M_COLOR["txt"],
        #     selectforeground=cm.M_COLOR["txt"],
        #     fieldforeground=cm.M_COLOR["txt"],
        #     fieldbackground=cm.M_COLOR["darker"],
        #     selectbackground=cm.M_COLOR["darker"],
        #     bordercolor=cm.M_COLOR["cbg"],
        #     relief="flat",
        #     troughcolor=cm.M_COLOR["cbg"],
        #     arrowcolor=cm.M_COLOR["txt"],
        #     arrowsize=16,
        #     gripcount=0,
        # )
        style.layout("EntryStyle.TEntry",
                     [('Entry.plain.field', {'children': [(
                         'Entry.background', {'children': [(
                             'Entry.padding', {'children': [(
                                 'Entry.textarea', {'sticky': 'nswe'})],
                                 'sticky': 'nswe'})], 'sticky': 'nswe'})],
                         'border': '0', 'sticky': 'nswe'})])
        self.scrollbar = ttk.Scrollbar(self.info_frame, orient=VERTICAL)
        self.items_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.items_listbox.yview)

        # Entries.
        self.class_entry = ttk.Entry(
            self.item_frame,
            width=10,
            font=cm.M_FONT,
            style="EntryStyle.TEntry",
        )
        self.description_entry = ttk.Entry(
            self.item_frame,
            width=24,
            font=cm.M_FONT,
            style="EntryStyle.TEntry",
        )
        self.value_entry = ttk.Entry(
            self.item_frame,
            width=8,
            font=cm.M_FONT,
            style="EntryStyle.TEntry",
        )
        self.date_entry = DateEntry(
            self.item_frame,
            width=8,
            font=cm.M_FONT,
            # date_pattern="dd/mm/yy",
            # style="EntryStyle.TEntry",
        )
        self.date_entry["borderwidth"] = 1
        self.date_entry["background"] = cm.M_COLOR["darker"]
        self.date_entry["foreground"] = cm.M_COLOR["txt"]
        self.sub_description_entry = ttk.Entry(
            self.item_frame,
            width=24,
            font=cm.M_FONT,
            style="EntryStyle.TEntry",
        )
        self.sub_value_entry = ttk.Entry(
            self.item_frame,
            width=8,
            font=cm.M_FONT,
            style="EntryStyle.TEntry",
        )
        self.type_list = ttk.Combobox(
            self.item_frame,
            width=8,
            font=cm.M_FONT,
            style="ComboBoxStyle.TCombobox",
            values=("Débito", "Crédito"),
            state="readonly",
        )
        self.type_list.set("Débito")

        # Buttons.
        self.add_item_button = self._button(frame=self.item_frame, text="Confirmar")
        self.add_sub_item_button = self._button(frame=self.item_frame, text="Subitem")
        self.cancel_button = self._button(frame=self.item_frame, text="Cancelar")
        self.delete_item_button = self._button(frame=self.info_frame, text="Excluir")
        self.edit_item_button = self._button(frame=self.info_frame, text="Editar")
        # self.graph_button = self._button(frame=self.info_frame, text='Editar')

        # Commands.
        self.add_item_button["command"] = self.add_items
        self.delete_item_button["command"] = self.del_item
        self.cancel_button["command"] = self.cancel
        self.add_sub_item_button["command"] = self.toggle_sub_item
        # self.sub_toggle_button['command'] =

        # Griding.
        self.class_lb.grid(row=0, column=0, sticky=W, padx=2)
        self.class_entry.grid(row=1, column=0, padx=2)
        self.description_lb.grid(row=0, column=1, sticky=W, padx=2)
        self.description_entry.grid(row=1, column=1, padx=2)
        self.sub_description_entry.grid(row=2, column=1, padx=2)
        self.value_lb.grid(row=0, column=2, sticky=W, padx=2)
        self.value_entry.grid(row=1, column=2, padx=2)
        self.sub_value_entry.grid(row=2, column=2, padx=2)
        self.type_lb.grid(row=0, column=3, sticky=W, padx=2)
        self.type_list.grid(row=1, column=3, sticky=W, padx=2)
        self.add_sub_item_button.grid(row=2, column=0, padx=2)
        self.date_lb.grid(row=0, column=4, sticky=W, padx=2)
        self.date_entry.grid(row=1, column=4, padx=2)
        self.add_item_button.grid(row=1, column=5, padx=2)
        self.cancel_button.grid(row=2, column=5, padx=2)

        self.items_listbox.grid(row=0, column=0, columnspan=7, sticky=NSEW)
        self.scrollbar.grid(row=0, column=6, sticky=N + S + E)
        self.get_items()
        self.toggle_sub_item()
        # self.get_sub_items()
        for item in self.items_list:
            self.update_string(last_item=item)
        self.delete_item_button.grid(row=1, column=6, sticky=E)
        self.edit_item_button.grid(row=1, column=6, sticky=W)
        self.message_lb.grid(row=1, column=0, sticky=W, columnspan=6)

        # Binds.
        # self.bind('<Control-s>', self.save)
        self.items_listbox.bind("<<ListboxSelect>>", self.listbox_callback)
        # self.items_listbox.bind('<FocusOut>', lambda: self.selected_item_index = 0)
        self.bind("<Return>", self.add_items)
        # self.bind('<Escape>', lambda k: cm.f_invoker(button=self.cancel_button))

    def add_items(self):
        """Add item and/or sub item list to database, considering the operation type
        (from type_list entry)."""
        # create a stringvar to represent op_type.
        operation_type = -1 if self.type_list.get() == "Débito" else 1
        items = self.description_entry.get().split(";")
        values = self.value_entry.get().split(";")
        print(values, items)
        if "" in items or "" in values or self.class_entry.get() == "":
            self.error_label(
                text="Os campos Classe, Descrição ou Valor precisam ser " "preenchidos."
            )
            self.description_entry.focus()
            return
        if len(items) != len(values):
            self.error_label(
                text="A quantidade de items na Descrição precisa ser igual "
                     "à quantidade de valores."
            )
            self.description_entry.focus()
            return
        if len(items) > 1 and (
                self.sub_description_entry.get() != "" or self.sub_value_entry.get() != ""
        ):
            self.error_label(
                text="Múltiplos produtos na Descrição não podem ter " "Subitems"
            )
            self.sub_description_entry.focus()
            return
        values = [float(k) for k in values]
        items_dict = dict(zip(items, values))
        items_list = [
            Item(
                customer_id=self.customer_id,  # 1 de teste
                date=datetime.combine(self.date_entry.get_date(), time()),
                kind=self.class_entry.get(),
                type=operation_type,
                description=i,
                value=operation_type * v,
            )
            for i, v in items_dict.items()
        ]
        try:
            self.add_sub_items(items_list)
            for item in items_list:
                create_item(item)
                self.get_items()
                Logger().log_it("kern", "info", f"Commit done: {item}.")
                self.update_string(item)
            self.cancel()
            self.class_entry.focus()
            print(self.add_sub_item)
            if self.add_sub_item:
                cm.f_invoker(self.add_sub_item_button)
        except ItemError as ie:
            self.error_label(text=str(ie.message))

    def add_sub_items(self, items_list):
        if len(items_list) > 1 or not self.add_sub_item:
            return
        item = items_list[0]
        products = self.sub_description_entry.get().split(";")
        sub_values = self.sub_value_entry.get().split(";")
        if "" in products or "" in sub_values:
            self.sub_description_entry.focus()
            raise ItemError(
                error_type="Subitem",
                message="Os campos Descrição ou Valor precisam ser preenchidos.",
            )
        if len(products) != len(sub_values):
            self.sub_value_entry.focus()
            raise ItemError(
                error_type="Subitem",
                message="Quantidade de produtos e valores diferentes!",
            )
        sub_values = [float(k) for k in sub_values]
        if abs(sum(sub_values) - item.type * item.value) >= 0.2:
            self.sub_value_entry.focus()
            raise ItemError(
                error_type="Subitem",
                message="Soma dos valores dos produtos diferente do valor do item!",
            )
        for sub_item in range(len(products)):
            print("subitemadded")
            last_sub_item = SubItem(
                item=item, description=products[sub_item], value=sub_values[sub_item]
            )
            create_sub_item(last_sub_item)
            self.get_items()
            Logger().log_it("kern", "info", f"Commit done: {last_sub_item}.")

    def error_label(self, text: str):
        print("error label")
        self.message_lb.config(text=text, fg=cm.M_COLOR["error"])
        self.after(100, lambda: self.message_lb.config(text=text, fg=cm.M_COLOR["txt"]))
        self.after(
            200, lambda: self.message_lb.config(text=text, fg=cm.M_COLOR["error"])
        )
        self.after(400, lambda: self.message_lb.config(text=text, fg=cm.M_COLOR["txt"]))
        self.after(3000, lambda: self.message_lb.config(text=""))

    def toggle_sub_item(self):
        self.add_sub_item = not self.add_sub_item
        print("add sub item?", self.add_sub_item)
        last_color = self.add_sub_item_button["background"]
        if last_color == cm.M_COLOR["darker"]:
            self.sub_description_entry.grid_remove()
            self.sub_value_entry.grid_remove()
            self.sub_description_entry.delete(0, END)
            self.sub_value_entry.delete(0, END)
            self.add_sub_item_button["background"] = self.bg_color
        elif last_color == self.bg_color:
            self.sub_description_entry.grid(row=2, column=1)
            self.sub_value_entry.grid(row=2, column=2)
            self.add_sub_item_button["background"] = cm.M_COLOR["darker"]

    def del_item(self):  # excluir subitems
        delete_item(self.items_list.pop(self.selected_item_index).id)
        self.items_listbox.delete(self.items_listbox.curselection()[0])
        self.get_items()
        self.items_listbox.selection_set(0)
        self.items_listbox.activate(0)
        self.listbox_callback()
        # self.items_listbox.see(1)

    def get_items(self):
        self.items_list = read_items()

    def get_sub_items(self):  #
        self.items_list = read_sub_items()

    def update_string(self, last_item):  # adicionar data a linha
        # if self.sub_items_list
        if type(last_item) == Item:
            type_text = "Item"
        else:
            type_text = "SubItem"
        line = f'{last_item.date.strftime("%d/%m/%Y")} — {type_text}: {last_item.kind}, {last_item.description}'
        self.items_listbox.insert(0, line)

    def listbox_callback(self, event=None):
        try:
            self.selected_item_index = (
                    len(self.items_list) - 1 - self.items_listbox.curselection()[0]
            )
            print(self.selected_item_index)
            print(self.items_list[self.selected_item_index])
        except IndexError:
            pass

    def cancel(self):
        self.class_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.sub_description_entry.delete(0, END)
        self.value_entry.delete(0, END)
        self.sub_value_entry.delete(0, END)
        self.class_entry.focus()

    def _label(self, frame, text, font=cm.M_FONT, anchor="w"):
        label = Label(
            frame,
            text=text,
            fg=cm.M_COLOR["txt"],
            bg=self.bg_color,
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
            activeforeground=self.bg_color,
        )
        return button
