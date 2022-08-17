from tkinter import *
import pandas as pd
from common import M_FONT, M_COLOR, resource_path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from processing.graph import Graph
from processing.database import read_items


class Toolbar(Frame):
    def __init__(self, master, customer):
        Frame.__init__(self, master)
        self.customer = customer
        self.master = master  # caso nao for usar tire
        self["bg"] = M_COLOR["darker"]
        self.items = pd.DataFrame()
        self.balance = 0
        self.graph = Graph(customer=self.customer)
        self.showing = False
        # Images.
        self.profile_img = PhotoImage(file=resource_path("images/profile.png"))
        self.refresh_img = PhotoImage(file=resource_path("images/refresh.png"))
        self.blur_img = PhotoImage(file=resource_path("images/blur.png"))
        # Canvas.
        self.graph_widget = None
        # self.graph_widget.draw()
        self.toolbar_canvas = Canvas(
            self,
            bg=M_COLOR["darker"],
            width=160,
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
            28, 24, image=self.blur_img, anchor=NW
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
            command=self.set_profile,
        )
        # Placing and packing.
        self.toolbar_canvas.pack()
        self.create_mini_plot()
        self.refresh_bt.place(x=135, y=0)
        self.profile_bt.place(x=4, y=60)
        # Binds.
        self.toolbar_canvas.tag_bind(
            self.balance_value_lb, "<ButtonPress-1>", self.view_balance_toggle
        )
        self.toolbar_canvas.tag_bind(
            self.blur, "<ButtonPress-1>", self.view_balance_toggle
        )

    def set_profile(self):
        # self.master.accounting.grid_forget()
        self.master.show_profile()

    def create_mini_plot(self):
        if self.graph_widget:
            self.graph_widget.destroy()
        self.graph.get_items()
        self.graph_widget = FigureCanvasTkAgg(
            self.graph.mini_graph, master=self
        ).get_tk_widget()
        self.graph_widget.pack(fill=BOTH)
        self.graph_widget.bind(
            "<ButtonPress-1>",
            self.open_graph,
        )

    def open_graph(self, event=None):
        self.graph.show()
        return event

    def refresh(self):
        # try:
        self.items = pd.DataFrame(
            [vars(field) for field in read_items(customer_id=self.customer.id)]
        )
        self.balance = self.items.value.sum()
        self.toolbar_canvas.itemconfig(self.updated_lb, text="...")
        self.toolbar_canvas.itemconfig(
            self.balance_value_lb, text=f"R$ {self.balance:9,.2f}"
        )
        self.create_mini_plot()
        self.after(
            100,
            lambda: self.toolbar_canvas.itemconfig(self.updated_lb, text="Atualizado"),
        )
        self.after(
            900,
            lambda: self.toolbar_canvas.itemconfig(self.updated_lb, text=""),
        )
        # except Exception as var_exception:
        #     self.toolbar_canvas.itemconfig(self.updated_lb, text="...")
        #     self.after(
        #         100,
        #         lambda: self.toolbar_canvas.itemconfig(
        #             self.updated_lb, text=f"Erro."
        #         ),
        #     )
        #     self.after(
        #         1200,
        #         lambda: self.toolbar_canvas.itemconfig(self.updated_lb, text=""),
        #     )

    def view_balance_toggle(self, event=None):
        if self.showing:  # unseen>seen
            self.toolbar_canvas.itemconfig(self.blur, state=NORMAL)
        else:
            self.refresh()
            self.toolbar_canvas.itemconfig(
                self.balance_value_lb, text=f"R$ {self.balance:9,.2f}"
            )
            self.after(
                300, lambda: self.toolbar_canvas.itemconfig(self.blur, state=HIDDEN)
            )
        self.showing = not self.showing
        return event
