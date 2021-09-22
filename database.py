import common as cm
import os
from sqlmodel import SQLModel, create_engine, Session, select
from models import Item, SubItem, Customer

db_name = "constancy"
db_path = cm.resource_path(f"{db_name}.db")
engine = create_engine(f"sqlite:///{db_name}.db", echo=True)


class DBError(Exception):
    pass


def create_db():
    print("creatin")
    if not os.path.exists(db_path):
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


def read_items(customer_id=1):
    with Session(engine) as session:
        query = select(Item).where(Item.customer_id == customer_id)
        # noinspection PyTypeChecker
        items = session.exec(query).all()
        return items


def read_sub_items():  # item_id: list
    with Session(engine) as session:
        query = select(SubItem)  # .where(Item.item_id in item_id)
        # noinspection PyTypeChecker
        sub_item = session.exec(query).all()
        return sub_item


# def read_customer():
#     with Session(engine) as session:
#         customer = session.exec(select(Customer)).all()
#         return customer


def reset_db():
    if os.path.exists(db_path):
        os.remove(db_path)
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
