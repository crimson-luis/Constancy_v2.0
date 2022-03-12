import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import mplcyberpunk
from database import read_items
from common import resource_path


class Graph:
    def __init__(self, customer):
        self.customer = customer
        self.items = pd.DataFrame()
        self.balance_series = pd.DataFrame()
        self.get_items()

    def get_items(self):
        self.items = pd.DataFrame(
            [vars(field) for field in read_items(customer_id=self.customer.id)]
        )
        self.balance_series = self.items.groupby(["date"]).sum().reset_index()
        self.balance_series.sort_values(by=["date"], inplace=True)

    def show(self):
        plt.close()
        plt.plot(
            self.balance_series["date"].dt.strftime("%d/%m/%y"),
            self.balance_series.value.cumsum(),
            "m",
            marker=".",
        )
        mplcyberpunk.add_glow_effects()
        plt.xticks(rotation=22)
        plt.subplots_adjust(right=0.95, top=0.93, bottom=0.15)
        plt.title("Saldo ao longo do tempo")
        fig = plt.gcf()
        manager = plt.get_current_fig_manager()
        manager.set_window_title(f"{self.customer.name} - Balance")
        manager.window.wm_iconbitmap(resource_path("images/icon.ico"))
        # manager.window.SetPosition()
        plt.ylim(bottom=0)
        plt.xlabel("Data")
        plt.ylabel("Saldo")
        plt.show()

    @property
    def mini_graph(self):
        plt.style.use("cyberpunk")
        mini_figure, mini_figure_axis = plt.subplots(1, 1, figsize=(1.55, 1))
        plt.plot(
            self.balance_series["date"].dt.strftime("%d/%m/%y"),
            self.balance_series.value.cumsum(),
            "m",
            marker="."
        )
        plt.xticks([])
        plt.yticks([])
        mini_figure_axis.set_facecolor("#24093e")
        mini_figure.patch.set_facecolor("#24093e")
        plt.setp(mini_figure_axis.get_xticklabels(), visible=False)
        plt.setp(mini_figure_axis.get_yticklabels(), visible=False)
        # mpl.rcParams.update(mpl.rcParamsDefault)
        return mini_figure


if __name__ == "__main__":
    pass
