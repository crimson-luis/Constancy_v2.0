import common as cm
import os

import pandas as pd
import datetime
from typing import Optional, List
from sqlmodel import (
    SQLModel,
    create_engine,
    Session,
    Field,
    Relationship,
    select,
)


DB_PATH = cm.resource_path("data/constancy.db")
# Creating object to handle communication with database.
engine = create_engine("sqlite:///data/constancy.db", echo=True)


# class Settings(SQLModel, table=True):
#     settings_id: Optional[int] = Field(default=None, primary_key=True)
#     theme: str
#     language: str
#     eyes: str
#     repass: str

# class Product(SQLModel, table=True):
#     product_id: Optional[int] = Field(default=None, primary_key=True)
#     product_name: str


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    email: str
    # settings_id: str

    items: List["Item"] = Relationship(back_populates="customer")


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[datetime.datetime] = datetime.datetime.now()
    # sub_item_qt: Optional[int] = 0
    kind: str
    type: int
    description: str
    # parcel: Optional[int] = 1  # se for maior que um criar n items um em cada mes.
    value: float

    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(back_populates="items")

    sub_items: List["SubItem"] = Relationship(back_populates="item")


class SubItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    # unit: Optional[int] = 1
    value: float
    # unit_value: Optional[float] = 1

    item_id: Optional[int] = Field(default=None, foreign_key="item.id")
    item: Optional[Item] = Relationship(back_populates="sub_items")


class DBError(Exception):
    pass


# def fetch_graph_data():
#     data = [k.dict() for k in read_items()]
#     df_data = pd.DataFrame.from_dict(data)  # .sort_values(by=['date'])
#     df_data["date"] = pd.to_datetime(df_data.date, format="%Y-%m-%d")
# by_date = df_data.groupby(['date'])
# last_day = max(df_data['date'])
# end_of_month = (last_day.replace(day=1) +
#                 pd.DateOffset(months=1) -
#                 dt.timedelta(days=1))
# forecast_date = pd.date_range(start=min(df_data['date']), end=end_of_month)
# observed_date = pd.date_range(start=min(df_data['date']), end=max(df_data['date']))
# values_list = []
# dataframe = df_data[["date", "value"]].groupby(
#     ["date"]
# )[["date", "value"]].sum().reset_index()
# series = pd.Series(dataframe.value, dtype="float64")
# cumulative_sum = series.cumsum()
# serialized_date = [dt.datetime.strftime(d, "%d/%m/%y") for d in dataframe.date]
# return cumulative_sum, serialized_date


def create_db():
    if not os.path.exists(DB_PATH):
        SQLModel.metadata.create_all(engine)


def create_user(customer: Customer):
    with Session(engine) as session:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer


def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def create_sub_item(sub_item: SubItem):
    with Session(engine) as session:
        session.add(sub_item)
        session.commit()
        session.refresh(sub_item)
        return sub_item


def read_items(customer_id):
    with Session(engine) as session:
        query = select(Item).where(Item.customer_id == customer_id)
        # noinspection PyTypeChecker
        items = session.exec(query).all()
        return items


def read_sub_items(item_id):  # item_id: list
    with Session(engine) as session:
        query = select(SubItem).where(Item.id in item_id)
        # noinspection PyTypeChecker
        sub_item = session.exec(query).all()
        return sub_item


def get_customer(name):  # item_id: list
    with Session(engine) as session:
        query = select(Customer).where(Customer.name == name)
        # noinspection PyTypeChecker
        customer = session.exec(query).all()
        return customer


# def read_customer():
#     with Session(engine) as session:
#         customer = session.exec(select(Customer)).all()
#         return customer


def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        create_db()


def delete_item(item_id):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise DBError("Item não existe.")
        session.delete(item)
        session.commit()
        return True


def delete_sub_item(sub_item_id):
    with Session(engine) as session:
        sub_item = session.get(SubItem, sub_item_id)
        if not sub_item:
            raise DBError("Subitem não existe.")
        session.delete(sub_item)
        session.commit()
        return True


def delete_customer(item_id):
    with Session(engine) as session:
        customer = session.get(Customer, item_id)
        if not customer:
            raise DBError("Usuário não existe.")
        session.delete(customer)
        session.commit()
        return True


def sqmodel_to_df(objs: List[SQLModel]) -> pd.DataFrame:
    """Convert a SQLModel objects into a pandas DataFrame."""
    records = [i.dict() for i in objs]
    df = pd.DataFrame.from_records(records)
    return df


if __name__ == "__main__":
    create_db()
