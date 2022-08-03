import unittest
from unittest.mock import patch, Mock
from client import *


def test_data():
    return {'phone': '123', 'password': '345'}


# def phone():
#     return 'phone':'123'
# def password():
#     return 345
class TestUser(unittest.TestCase):

    # data={'phone':'123','password':'345'}

    @patch('builtins.input', return_value='123')
    def test_0_author(self, mock_input):
        query_client = {}
        result = author(query_client)
        ex_result = {'data': {'password': '123', 'phone': '123'}}
        {'command': 'auth', 'data': {'phone': '123', 'password': '123'}}
        {'command': 'auth', 'data': {'phone': '123', 'password': '123'},
         'i_key': '490527b2f023067f845cbc694f82d021afbacb3e', 'token': 'ea135929105c4f29a0f5117d2960926f'}

        self.assertEqual(result, ex_result)

    # @patch('soc.recv(1024)', return_value={'command': 'auth', 'data': {'phone': '123', 'password': '123'}})
    # def test_1_edit_profile(self):
    #     data = {'name': 'Татьяна'}
    #
    #     result = edit_profile(data)
    #     ex_result = {'name': 'Татьяна'}
    #     self.assertEqual(result, ex_result)

    def test_9_out(self):
        data = {'password': '123', 'phone': '123'}
        result = out(data)
        ex_result = {}
        self.assertEqual(result, ex_result)
    #
    # def test_send_get(self):
    #     data = {}
    #     result = send_get(data)
    #     ex_result = {}
    #     self.assertEqual(result, ex_result)


if __name__ == '__main__':
    unittest.main()
