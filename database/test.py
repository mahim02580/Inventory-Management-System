from datetime import date, time, datetime
from sqlalchemy import ForeignKey, Date, Time, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from unicodedata import category


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    code: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    base_unit_type: Mapped[str] = mapped_column()
    sell_unit_type: Mapped[str] = mapped_column()
    sell_unit_price: Mapped[float] = mapped_column()
    conversion_factor: Mapped[float] = mapped_column()
    pcs_per_box: Mapped[int] = mapped_column()
    current_stock: Mapped[float] = mapped_column()
    low_stock_alert: Mapped[float] = mapped_column()


engine = create_engine("sqlite:///database2.db")
Base.metadata.create_all(engine)
session = Session(engine)

products = session.execute(select(Product)).scalars().all()


engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
session = Session(engine)

for product in products:
    product = Product(category=product.category, name=product.name, base_unit_type=product.base_unit_type,
                      sell_unit_type=product.sell_unit_type, sell_unit_price=product.sell_unit_price, conversion_factor=product.conversion_factor, pcs_per_box=product.pcs_per_box,
                      current_stock=product.current_stock, low_stock_alert=product.low_stock_alert)
    session.add(product)
    session.commit()