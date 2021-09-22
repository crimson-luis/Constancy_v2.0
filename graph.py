import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

# import PIL
import mplcyberpunk

# import matplotlib
from database import read_items

# from numpy import arange, sin, pi
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
# matplotlib.use('TkAgg')

data = [k.dict() for k in read_items()]
df_data = pd.DataFrame.from_dict(data)  # .sort_values(by=['date'])
df_data["date"] = pd.to_datetime(df_data.date, format="%Y-%m-%d")
# by_date = df_data.groupby(['date'])
# last_day = max(df_data['date'])
# end_of_month = last_day.replace(day=1) + pd.DateOffset(months=1) - dt.timedelta(days=1)
# forecast_date = pd.date_range(start=min(df_data['date']), end=end_of_month)
# observed_date = pd.date_range(start=min(df_data['date']), end=max(df_data['date']))
# values_list = []


def f_graph(dataframe=df_data[["date", "value"]], show=True):
    dataframe = dataframe.groupby(["date"])[["date", "value"]].sum().reset_index()
    series = pd.Series(dataframe.value, dtype="float64")
    serialized_date = [dt.datetime.strftime(d, "%d/%m/%y") for d in dataframe.date]
    plt.style.use("cyberpunk")
    fig, axis = plt.subplots(1, 1, figsize=(1.55, 1))
    plt.plot(serialized_date, series.cumsum(), "m", marker=".")
    # mplcyberpunk.add_glow_effects()
    if show:
        plt.xticks(rotation=20)
        plt.subplots_adjust(right=0.95, top=0.93, bottom=0.15)
        plt.title("Balance over time")
        manager = plt.get_current_fig_manager()
        manager.set_window_title("Constancy - Balance")
        # manager.window.wm_iconbitmap(resource_path('icon.ico'))
        # manager.window.SetPosition()
        plt.ylim(bottom=0)
        plt.xlabel("Date")
        plt.ylabel("Balance")
        # plt.xticks([])
        # plt.yticks([])
        plt.show()
    else:
        plt.xticks([])
        plt.yticks([])
        axis.set_facecolor("#24093e")
        fig.patch.set_facecolor("#24093e")
        plt.setp(axis.get_xticklabels(), visible=False)
        plt.setp(axis.get_yticklabels(), visible=False)
        return fig
    # img = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())


# print(f_graph())
