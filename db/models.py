import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

"""
Модуль в котором описаны модели для базы даных парсера новостных сайтов.
Отношение между таблицами: один-ко-многим
"""

Base = declarative_base()


class Resource(Base):
    """Дочерний класс от declarative_base. Хранит сведения о новостных ресурсах"""
    __tablename__ = 'resource'

    RESOURCE_ID = sq.Column(sq.Integer(), primary_key=True, autoincrement=True)
    RESOURCE_NAME = sq.Column(sq.VARCHAR(255), nullable=True, default=None)
    RESOURCE_URL = sq.Column(sq.VARCHAR(255), nullable=True, default=None)
    top_tag = sq.Column(sq.VARCHAR(255), nullable=False)
    bottom_tag = sq.Column(sq.VARCHAR(255), nullable=False)
    title_cut = sq.Column(sq.VARCHAR(255), nullable=False)
    date_cut = sq.Column(sq.VARCHAR(255), nullable=False)


class Items(Base):
    """Дочерний класс от declarative_base. Хранит сведения о статьях"""
    __tablename__ = 'items'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    res_id = sq.Column(sq.Integer, sq.ForeignKey(Resource.RESOURCE_ID), nullable=False)
    link = sq.Column(sq.VARCHAR(255), nullable=False)
    title = sq.Column(sq.TEXT(), nullable=False)
    content = sq.Column(sq.TEXT(), nullable=False)
    nd_date = sq.Column(sq.BIGINT, nullable=False)
    s_date = sq.Column(sq.BIGINT, default=datetime.now().timestamp())
    not_date = sq.Column(sq.VARCHAR(25), nullable=False)

    res = relationship('Resource', backref='items')
    
class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(60), nullable=False)

    def __str__(self):
        return f"(id: {self.id}, name: {self.name})"


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(100), nullable=False)
    publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher_id = relationship('Publisher', backref='book_id')

    def __str__(self):
        return f"(id: {self.id}, title: {self.title}, id_publisher: {self.publisher_id})"


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(60), nullable=False)

    def __str__(self):
        return f"(id: {self.id}, name: {self.name})"


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    shop_id = relationship('Shop', backref='book_stock')
    book_id = relationship('Book', backref='shop_stock')

    def __str__(self):
        return f"(id: {self.id}, id_book: {self.book_id}," \
               f"id_shop: {self.shop_id}, count: {self.count})"


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL(6, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime)
    count = sq.Column(sq.Integer, nullable=False)
    stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    stock_id = relationship('Stock', backref="sale_id")

    def __str__(self):
        return f"(id: {self.id}, price: {self.price}, date_sale: {self.date_sale}," \
               f"id_stock: {self.stock_id}, count: {self.count})"


def create_tables(engine):
    """Функция для создания моделей в БД"""
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    pass
