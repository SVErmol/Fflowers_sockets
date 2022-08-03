import json
import socket
from os import urandom
import binascii
global URL
import requests

# soc = socket.socket()

URL = 'http://127.0.0.1:5000'

def client_connect():

    # soc.connect(('127.0.0.1', 8000))

    query_client = {}

    while 1:

        print()
        if (query_client == {}) or not ('token' in query_client):

            print("Авторизиризация")
            task = 0

        else:
            print("Выберите действие:")
            print("1-Просмотреть список заказов")
            print("2-Просмотреть данные заказа")
            print("3-Изменить комментарий к заказу")
            print("4-Изменить статус заказа")
            print("5-Посмотреть содержимое заказа")
            print("6-Изменить личный профиль")
            print("7-Поменять пароль")
            print("8-Выйти из личного кабинета")

            task = int(input())

        # soc.sendall(bytes(task,'UTF-8'))
        menu_dict = {
            0: ['auth', author],
            1: ['all_orders', all_orders],
            2: ['get_order', get_order],
            3: ['edit_note', edit_note],
            4: ['edit_status', edit_status],
            5: ['order_content', order_content],
            6: ['edit_profile', edit_profile],
            7: ['edit_password', edit_password],
            8: ['out', out]
        }



        try:
            # mail()
            md = menu_dict.get(task)
            query_client["command"] = md[0]

            query_client = md[1](query_client)
        except:
            if query_client["command"] != 'auth':
                print('Введите команду правильно')
            else:
                print('Неправильный логин или пароль')

 # # ____________________
 #        def mail():
 #            conn = pika.BlockingConnection(pika.ConnectionParameters(
 #                host='127.0.0.1', port=8000))
 #            channel = conn.channel()
 #
 #            channel.queue_declare(queue='test_persistent', durable=True)
 #
 #            def callback(ch, method, properties, body):
 #                '' 'Функция обратного вызова, обработка сообщений, взятых из rabbitmq' ''
 #                print(" [x] Received %r" % body)
 #                # time.sleep(5)
 #                ch.basic_ack(delivery_tag=method.delivery_tag)  # Отправить подтверждающее сообщение
 #
 #            channel.basic_qos(prefetch_count=1)
 #            channel.basic_consume(callback, queue='test_persistent', no_ack=False)
 #            print(' [*] Waiting for messages. To exit press CTRL+C')
 #            channel.start_consuming()  # Начните слушать, чтобы принять сообщение
 #
 #            pika.exceptions.ChannelClosed: (
 #                406, "PRECONDITION_FAILED - parameters for queue 'test_persistent' in vhost '/' not equivalent")
 #            # _________________________________
def out(query_client):
    """

    :param query_client: запрос пользователя
    :return:
    """
    # print(query_client)
    query_client = {}

    return query_client


def print_order(order):
    """

      :param query_client: объект типа Order
      :return: выведенная информация о заказе
      """
    print('Id курьера: ', order['courier_id'])
    print('Id флориста: ', order['florist_id'])
    print('Id клиента: ', order['client_id'])
    print('Адрес: ', order['address'])
    print('Дата заказа: ', order['date_order'])
    print('Дата доставки: ', order['date_delivery'])
    print('Дата оплаты: ', order['date_pay'])
    print('Сумма заказа: ', order['sum'])
    print('Статус заказа: ', status_order(order['status_order']))
    print('Примечание: ', order['note'])


def send_get(query_client):
    """

    :param query_client: запрос пользователя
    :return: ответ сервера
    """
    json_client = json.dumps(query_client)
    # soc.sendall(bytes(json_client, 'UTF-8'))

    # query_client = soc.recv(1024).decode()
    json_client = json.loads(query_client)
    return json_client


def status_order(json_client):
    """

    :param query_client: запрос пользователя
    :return: изменный статус заказа
    """
    if (json_client == 0):
        status_ord = 'Принят'
    else:
        status_ord = 'Доставлен'
    return status_ord


def show(json_client):
    """

    :param query_client: запрос пользователя
    :return: изменненный статус видимости
    """
    if (json_client == 0):
        status_ord = 'Скрыто'
    else:
        status_ord = 'Не скрыто'
    return status_ord


def author(query_client):
    """

    :param query_client: запрос пользователя на авторизацию
    :return: авторизированный пользователь
    """
    url = URL + '/authorization'
    data = {}
    data["phone"] = str(input("Введите логин:"))
    data["password"] = str(input("Введите пароль:"))

    # query_client['data'] = data
    json_client = requests.post(url, data=data)
    query_client["i_key"] = binascii.hexlify(urandom(20)).decode()
    print()
    print('Добро пожаловать')
    query_client["token"] = json_client['data']['token']

    return query_client


def get_order(query_client):
    """

      :param query_client: запрос пользователя
      :return: информация о заказе
      """
    print('Введите id заказа')
    task_order = input()
    task_order = int(task_order)
    data = {}
    data['id'] = task_order
    query_client['data'] = data
    json_client = send_get(query_client)
    print_order(json_client['data'])

    return query_client


def all_orders(query_client):
    """

      :param query_client: запрос пользователя
      :return: информация о заказах
      """

    url = URL + '/orders'
    response = requests.get(url)

    for order in response.text:
        print('Id заказа:', order['id'])

        print_order(order)
        print()
    return query_client


def edit_note(query_client):
    """

      :param query_client: запрос пользователя
      :return: измененный комментарий заказа
      """
    data = {}

    print('Введите id заказа')
    data['id'] = input()
    print("Введите примечание")
    data['note'] = input()

    query_client['data'] = data

    json_client = send_get(query_client)
    print('Примечание заказа №',
          json_client['data']['id'], 'успешно изменено')
    return json_client


def edit_status(query_client):
    """

        :param query_client: запрос пользователя
        :return: измененный статус заказа
        """
    data = {}

    print('Введите id заказа')
    data['id'] = input()
    print("Введите статус")
    print("0-Принят")
    print("1-Доставлен")
    data['status_order'] = input()
    query_client['data'] = data

    json_client = send_get(query_client)
    print('Статус заказа №',
          json_client['data']['id'], 'успешно изменен')
    return json_client


def order_content(query_client):
    """

        :param query_client: запрос пользователя
        :return: содержимое заказа
        """
    data = {}
    print('Введите id заказа')
    task_order = input()
    task_order = int(task_order)
    data = {}
    data['id_order'] = task_order
    query_client['data'] = data

    json_client = send_get(query_client)
    for product in json_client['data']:
        print_product(product)
    return json_client


def print_product(product):
    print()
    print('Id товара:', product['id'])
    print('Название товара:', product['name'])
    print('Категория товара:', product['subcategory_id'])
    print('Описание товара:', product['description'])
    print('Id поставщика:', product['supplier_id'])
    print('Цена:', product['price'])
    print('Отображение:', show(product['show']))
    print('Артикул товара:', product['article'])


def edit_profile(query_client):
    """

        :param query_client: запрос пользователя
        :return: измененный профиль пользователя
        """
    data = {}

    print('Введите имя')
    data['name'] = input()

    query_client['data'] = data

    json_client = send_get(query_client)
    print("Ваши данные успешно изменены")
    return json_client


def edit_password(query_client):
    """

           :param query_client: запрос пользователя
           :return: измененный пароль пользователя
           """
    data = {}
    print('Введите старый пароль')
    data['old_password'] = input()
    print('Введите новый пароль')
    data['new_password'] = input()
    print('Подтвердите новый пароль')
    data['new_password1'] = input()
    query_client['data'] = data

    json_client = send_get(query_client)
    print("Ваш пароль успешно изменен")
    return json_client


client_connect()
