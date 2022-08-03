import json


import yaml


from sqlalchemy import ForeignKey, create_engine, Integer, String, Boolean, Date, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship, scoped_session
import hashlib

import logging
from memcache import *
from flask import Flask,request


app = Flask(__name__)


with open('settings') as conf:
    # config = configparser.ConfigParser()
    conf = yaml.safe_load(conf)
salt = conf['salt']

file_log = logging.FileHandler('log.log')
console_log = logging.StreamHandler()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%d.%b.%Y %H:%M:%S",
    handlers=(file_log, console_log))
log = logging.getLogger('server')

# e = create_engine("sqlite:///mydatabase.db")

# e = create_engine("postgresql+psycopg2://postgres:123@localhost/postgres")

Base = declarative_base()

client = conf['client']

# client.set('some_key', 'some value')

# client.get('some_key') # 'some value'

s = Session(bind=create_engine(conf['engine_sqlite']))


# session_factory = sessionmaker(bind=create_engine)
# s = scoped_session(session_factory)

def object_to_dict(ob):
    """
    Метод для преобразования объекта в словарь
    :param ob: объект
    :return: словарь
    """
    return {x.name: (str(getattr(ob, x.name)))
            for x in ob.__table__.columns
            }


class User(Base):
    """
    Класс пользователя

    id-id пользователя
    surname-фамилия пользователя
    name-имя пользователя
    patronymic-отчество пользователя
    phone-номер телефона
    birthday-дата рождения
    password-пароль
    token-токен
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    surname = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    patronymic = Column(String(250), nullable=False)
    phone = Column(String(250), nullable=False)
    birthday = Column(Date, nullable=False)
    password = Column(String(250), nullable=False)
    token = Column(String(250), nullable=False)

    order = relationship("Order", back_populates='courier')

    @app.route('/authorization', methods=['POST'])
    def auth():
        """
        Метод для авторизации пользователя
         :return:
         :param data: словарь с номером телефона и паролем
        :return: словарь с информацией о пользователе
        """
        data = json.loads(request.form["data"].replace("'", '"'))
        user = s.query(User).filter(User.phone == data["data"]['phone']).first()
        salt_ = hashlib.sha256(
            data["data"]['password'].encode() + salt.encode()).hexdigest()
        if user.password == salt_:
            data["data"] = object_to_dict(user)
            data["data"]['password'] = user.password

            return data
    @app.route('/edit_profile', methods=['POST'])

    def edit_profile():
        """

        :param courier: объект типа User
                data: словарь с информацией, которую хочет изменить пользователь
        :return: data: словарь с измененной информацией
        """
        data = json.loads(request.form["data"].replace("'", '"'))
        courier = s.query(User).filter(User.token == data['token']).first()
        courier.name = data['data']['name']

        s.add(courier)
        s.commit()
        data['data']=object_to_dict(courier)

        return data
    @app.route('/edit_password', methods=['POST'])

    def edit_password():
        """

              :param courier: объект типа User
                      data: словарь с новым и старым паролем
              :return: data: словарь с измененным паролем
              """
        data = json.loads(request.form["data"].replace("'", '"'))
        courier = s.query(User).filter(User.token == data['token']).first()


        data["data"]['new_password1'] = hashlib.sha256(
            data["data"]['new_password1'].encode() + salt.encode()).hexdigest()
        data["data"]['new_password'] = hashlib.sha256(
            data["data"]['new_password'].encode() + salt.encode()).hexdigest()
        data["data"]['old_password'] = hashlib.sha256(
            data["data"]['old_password'].encode() + salt.encode()).hexdigest()
        if courier.password == data["data"]['old_password'] and data["data"]['new_password'] == data["data"]['new_password1']:
            courier.password = data["data"]['new_password']
            s.add(courier)
            s.commit()
            return data


class Order(Base):
    """
    Класс заказа

    id-id заказа
    courier_id-id курьера
    florist_id-id флориста
    client_id-id клиента
    address-адрес заказа
    date_order-дата заказа
    date_delivery-дата доставки
    date_pay-дата оплаты
    sum-сумма оплаты
    status_order-статус заказа
    note-комментарий

    """
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    florist_id = Column(Integer, nullable=True)
    client_id = Column(Integer, nullable=True)
    address = Column(String(250), nullable=False)
    date_order = Column(Date, nullable=False)
    date_delivery = Column(Date, nullable=False)
    date_pay = Column(Date, nullable=False)
    sum = Column(Integer, nullable=False)
    status_order = Column(Integer, nullable=False)
    note = Column(String(250), nullable=False)

    courier = relationship("User", back_populates="order")

    content_order = relationship("OrderContent", back_populates='order')


    @app.route('/orders', methods=['POST'])

    def all_orders():
        """

          :param courier: объект типа User
                      data: словарь с данными
        :return: data: словарь с информацией о заказаз курьера
        """
        data = json.loads(request.form["data"].replace("'", '"'))
        courier = s.query(User).filter(User.token == data['token']).first()
        orders = courier.order
        new_orders = []  # [{} {} {}]
        for order in orders:
            data['data'] = object_to_dict(order)
            # data = Order.print_order(order, data)

            new_orders.append(data['data'])
        data['data'] = new_orders
        return data
    @app.route('/orders/order', methods=['POST'])

    def get_order():
        """

               :param courier: объект типа User
                           data: словарь с данными о номере заказа
             :return: data: словарь с информацией о контретном заказе

             """

        data = json.loads(request.form["data"].replace("'", '"'))
        courier = s.query(User).filter(User.token == data['token']).first()
        order = s.query(Order).get(data['data']['id'])
        if order in courier.order:
            data['data'] = object_to_dict(order)

            return data
    @app.route('/orders/order/edit_note', methods=['POST'])

    def edit_note():
        """

                    :param courier: объект типа User
                                data: словарь с данными о номере заказа и комментарии
                  :return: data: словарь с информацией измененного заказа
                  """
        data = json.loads(request.form["data"].replace("'", '"'))
        courier = s.query(User).filter(User.token == data['token']).first()
        order = s.query(Order).get(data['data']['id'])

        if order in courier.order:
            order.note = data['data']['note']
            s.add(order)

            s.commit()
            data['data']=object_to_dict(order)
            return data
    @app.route('/orders/order/edit_status', methods=['POST'])

    def edit_status():
        """

                         :param courier: объект типа User
                                     data: словарь с данными о номере заказа и статусе
                       :return: data: словарь с информацией измененного заказа
                       """
        data = json.loads(request.form["data"].replace("'", '"'))
        courier = s.query(User).filter(User.token == data['token']).first()
        order = s.query(Order).get(data['data']['id'])
        if order in courier.order:
            order.status_order = data['data']['status_order']
            s.add(order)
            s.commit()
            data['data']=object_to_dict(order)

            return data


class Product(Base):
    """
     Класс товара

     id-id товара
     name-название товара
     subcategory_id-id категории
     photos-фото
     description-описание
     supplier_id-id поставщика
     price-цена
     show-скрывать/показывать
     article-артикул

     """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    subcategory_id = Column(Integer, nullable=False)
    photos = Column(String(250), nullable=True)
    description = Column(String(250), nullable=False)
    supplier_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    show = Column(Integer, nullable=False)
    article = Column(Integer, nullable=False)

    content_product = relationship("OrderContent", back_populates='product')


class OrderContent(Base):
    """
     Класс содержимого заказа

     id-id
     order_id-id
     product_id-id товара
     quanity-количество


     """
    __tablename__ = 'ordercontent'
    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quanity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="content_order")
    product = relationship("Product", back_populates="content_product")


    @app.route('/orders/order/content', methods=['POST'])

    def order_content():
        """

         :param courier: объект типа User
                                     data: словарь с данными о номере заказа
                       :return: data: словарь с информацией о заказе
        """
        data = json.loads(request.form["data"].replace("'", '"'))
        courier = s.query(User).filter(User.token == data['token']).first()
        order = s.query(Order).get(data['data']['id_order'])
        if order in courier.order:

            order_c = order.content_order
            new_orders = []  # [{} {} {}]
            for product in order_c:
                data = {}
                product_ = s.query(Product).get(product.product_id)
                data['data'] = object_to_dict(product_)
                new_orders.append(data['data'])
            data['data'] = new_orders

            return (data)


# Base.metadata.create_all(e)
client_count = threading.BoundedSemaphore(2)

