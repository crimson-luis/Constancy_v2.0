from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
import datetime

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
    date: Optional[datetime.datetime] = datetime.datetime.now().date()
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
