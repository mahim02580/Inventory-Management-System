import datetime
from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ------------------------------------------Table Models------------------------------------------
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column("ID", primary_key=True)
    name: Mapped[str] = mapped_column("Name", nullable=False)
    unit_price: Mapped[int] = mapped_column("Unit Price", nullable=False)
    stock: Mapped[int] = mapped_column("Stock", nullable=False)


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column("ID", primary_key=True)
    name: Mapped[str] = mapped_column("Name")
    phone: Mapped[str] = mapped_column("Phone")
    address: Mapped[str] = mapped_column("Address")
    purchases = relationship("Purchase", back_populates="customer")


class Purchase(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column("ID", primary_key=True)
    date: Mapped[str] = mapped_column("Date", nullable=False)
    time: Mapped[str] = mapped_column("Time", nullable=False)
    details: Mapped[str] = mapped_column("Details", nullable=False)
    customer_id: Mapped[int] = mapped_column("Customer ID", ForeignKey(Customer.id))
    customer = relationship("Customer", back_populates="purchases")
    mrp_total: Mapped[int] = mapped_column("MRP Total", nullable=False)
    discount: Mapped[int] = mapped_column("(-) Discount", nullable=False)
    total_payable: Mapped[int] = mapped_column("Total Payable", nullable=False)
    total_paid_amount: Mapped[int] = mapped_column("Paid", nullable=False)
    change_amount: Mapped[int] = mapped_column("Change", nullable=False)
    due_amount: Mapped[int] = mapped_column("Due", nullable=False)


# ------------------------------------------ Engine + Session ------------------------------------------
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
session = Session(engine)


# ------------------------------------------Functions------------------------------------------
# Product Management
def get_product_by_name(product_name):
    """Gets a specific product using product_name"""
    product = session.execute(select(Product).where(Product.name == product_name)).scalar()
    return product


def get_all_products_name():
    """Gets all products name available in the products table"""
    return session.execute(select(Product.name)).scalars().all()


def get_all_products():
    products = session.execute(select(Product)).scalars().all()
    return products


def add_product(product):
    session.add(product)
    session.commit()


def update_product(product_id, changed_column, new_value):
    product_to_update = session.get(Product, product_id)
    product_to_update.__setattr__(changed_column, new_value)
    session.commit()


def delete_product(product_id):
    product_to_delete = session.get(Product, ident=product_id)
    session.delete(product_to_delete)
    session.commit()


def adjust_stock_of_product(product_id, quantity):
    product = session.get(Product, int(product_id))
    product.stock -= quantity
    session.commit()


def update_stock_of_product(product_name, new_stock):
    product = get_product_by_name(product_name)
    product.stock += int(new_stock)
    session.commit()


# Customer Management
def get_customer_by_phone(customer_phone):
    customer = session.execute(select(Customer).where(Customer.phone == customer_phone)).scalar()
    return customer


def add_customer(customer):
    session.add(customer)
    session.commit()
    return customer


# Sales Management
def add_purchase(purchase):
    session.add(purchase)
    session.commit()
    return purchase


def get_today_sales():
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    today_sales = session.execute(select(Purchase).where(Purchase.date == today)).scalars().all()
    return today_sales


def get_all_sales():
    all_sales = session.execute(select(Purchase)).scalars().all()
    return all_sales
