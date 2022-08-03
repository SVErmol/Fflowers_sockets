import json
import win32api
from winerror import ERROR_ALREADY_EXISTS
import win32event

from exceptions import *
from models import *
#from memcache import *

#import pika


def server_connect():
    # ADDRESS = '127.0.0.1'
    # PORT = 8000

    # port = conf['port']
    # address = conf['address']
    #
    # soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # soc.bind((address, port))
    #
    # soc.listen()

    log.info('Work:' + str('127.0.0.1'))

    while 1:
        # connection, address = soc.accept()
        # t = threading.Thread(target=server_t, args=(connection, address))
        # t.start()
        print('client connection', '127.0.0.1')
        #     #_______________________________________________
        # connect = pika.BlockingConnection(pika.ConnectionParameters(
        #     host=address, port=port, ))  # Определить пул соединений
        # channel = connect.channel()  # Объявить очередь на отправку сообщений в нее

        # channel.queue_declare(queue='test_persistent', durable=True)
        # for i in range(10):
        #     channel.basic_publish(exchange='', routing_key='test_persistent', body=str(i),
        #                           properties=pika.BasicProperties(delivery_mode=2))
        #     print('send success msg[%s] to rabbitmq' % i)
        # connection.close()
    # #____________________________________________________


def server_t(connection, address):
    menu_dict = {
        'auth': User.auth,
        'all_orders': Order.all_orders,
        'get_order': Order.get_order,
        'edit_note': Order.edit_note,
        'edit_status': Order.edit_status,
        'order_content': OrderContent.order_content,
        'edit_profile': User.edit_profile,
        'edit_password': User.edit_password
    }
    while 1:
        try:
            query_client = connection.recv(1024)
            decode_query = query_client.decode()

            json_query = json.loads(decode_query)
            print(json_query)
        except:
            log.error('Error!')

        if not json_query:
            log.info('Disconnected:' + str(address))
            break
        try:
            com = json_query['command']
            if com == 'auth':
                json_query['data'] = menu_dict.get(
                    com)(json_query['data'])
                print(json_query)

            else:
                courier = s.query(User).filter(
                    User.token == json_query['token']).first()
                json_query['data'] = menu_dict.get(
                    com)(json_query['data'], courier)
        except NotFoundError as er:
            json_query['message'] = er.message
            log.warning('Not Found!')
        except InternalServerError as er:
            json_query['message'] = er.message
        except ErrorUnauthorized as er:
            json_query['message'] = er.message
            log.error('Unauthorized Error!')
        try:
            connection.sendall(bytes(json.dumps(json_query), 'UTF-8'))
        except:
            log.error('Sending Error!')
        print(json_query)


class single_example:
    def __init__(self):
        self.mutex_name = "testmutex_{b5123b4b-e59c-4ec7-a912-51be8ebd5819}"
        self.mutex = win32event.CreateMutex(None, 1, self.mutex_name)
        self.last_error = win32api.GetLastError()

    def already_working(self):
        return (self.last_error == ERROR_ALREADY_EXISTS)


app_ = single_example()
if app_.already_working():
    print("Server is running")
    exit(0)
if __name__ == '__main__':
    app.run()
