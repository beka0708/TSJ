import hashlib
import random
import string
from datetime import timedelta
from django.utils import timezone
import xml.etree.ElementTree as ET
from django.conf import settings
import requests
from django.urls import reverse_lazy


class FreedomPay:
    def __init__(self):
        self._merchant_id = settings.MERCHANT_ID
        self._secret_key = settings.PAY_SECRET_KEY
        self._pg_success_url = settings.PG_SUCCESS_URL
        self._pg_failure_url = settings.PG_FAILURE_URL
        self._pg_back_link = settings.PG_BACK_LINK

    @property
    def merchant_id(self):
        return self._merchant_id

    @property
    def secret_key(self):
        return self._secret_key

    @property
    def pg_success_url(self):
        return self._pg_success_url

    @property
    def pg_failure_url(self):
        return self._pg_failure_url

    @property
    def pg_back_link(self):
        return self._pg_back_link

    def generate_signature(self, params, operation_type):
        """
        Генерирует подпись для запроса к API FreedomPay.

        :param params: Словарь параметров запроса.
        :param operation_type: Тип операции.
        :return: Подпись запроса.
        """
        values_list = [operation_type] + [str(v) for k, v in sorted(params.items())] + [self.secret_key]
        signature_base = ';'.join(values_list)
        signature = hashlib.md5(signature_base.encode()).hexdigest()
        return signature

    def generate_random_string(self, length=12):
        """Генерирует случайную строку заданной длины."""
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return result_str

    def send_request(self, url, params, operation_type):
        """
        Общий метод для отправки HTTP-запросов к платежному API.

        :param url: Url, к которому идет обращение.
        :param params: Словарь параметров запроса.
        :param operation_type: Тип операции для генерации подписи.
        :return: Объект ответа от сервера.
        """
        salt = self.generate_random_string()
        params.update({
            'pg_merchant_id': self.merchant_id,
            'pg_salt': salt,
        })
        signature = self.generate_signature(params, operation_type)
        params['pg_sig'] = signature
        response = requests.post(url, data=params)
        response.encoding = 'utf-8'
        return response

    def init_payment_online(self, amount, order_id, user_id, description):
        pg_result_url = f"http://113.30.190.31:8001/"
        url = f"https://api.paybox.money/init_payment.php"
        params = {
            'pg_amount': str(amount),
            'pg_order_id': str(order_id),
            'pg_user_id': str(user_id),
            'pg_description': description,
            'pg_currency': 'KGS',
            'pg_result_url': str(pg_result_url),
            # 'pg_success_url': self.pg_success_url,
            # 'pg_failure_url': self.pg_failure_url,
            'pg_auto_clearing': 1
        }
        return self.send_request(url, params, 'init_payment.php')

    def init_payment(self, amount, order_id, user_id, card_token, description):
        pg_result_url = reverse_lazy('payment_result')
        url = f"https://api.freedompay.money/v1/merchant/{self.merchant_id}/card/init"
        params = {
            'pg_amount': str(amount),
            'pg_order_id': str(order_id),
            'pg_user_id': str(user_id),
            'pg_card_token': card_token,
            'pg_description': description,
            'pg_currency': 'KGS'
            # 'pg_result_url': str(pg_result_url),
            # 'pg_success_url': self.pg_success_url,
            # 'pg_failure_url': self.pg_failure_url
        }
        return self.send_request(url, params, 'init')

    def do_capture(self, pg_payment_id, pg_clearing_amount):
        url = f"https://api.freedompay.money/do_capture.php"
        params = {
            'pg_payment_id': pg_payment_id,
            'pg_clearing_amount': pg_clearing_amount,
        }
        return self.send_request(url, params, 'do_capture.php')

    def cancel(self, pg_payment_id):
        url = f"https://api.freedompay.money/cancel.php"
        params = {
            'pg_payment_id': pg_payment_id
        }
        return self.send_request(url, params, 'cancel.php')

    def complete_payment(self, payment_id):
        url = f"https://api.freedompay.money/v1/merchant/{self.merchant_id}/card/direct"
        params = {
            'pg_payment_id': str(payment_id),
        }
        return self.send_request(url, params, 'direct')

    def get_payment_status(self, payment_id):
        """
        Получает статус платежа по его ID.

        :param payment_id: ID платежа.
        :return: XML-ответ от платежной системы.
        """
        url = "https://api.freedompay.money/get_status3.php"
        params = {
            'pg_payment_id': payment_id
        }
        response = self.send_request(url, params, 'get_status3.php')
        response_xml = ET.fromstring(response.content.decode())
        return response_xml

    def payout_to_unsaved_card(self, amount, order_id, description):
        """
        Осуществляет выплату на несохраненную карту.

        :param amount: Сумма выплаты.
        :param order_id: ID выплаты.
        :param description: Описание выплаты.
        """
        order_time_limit = timezone.now() + timedelta(days=1)
        order_time_limit = order_time_limit.strftime('%Y-%m-%d %H:%M:%S')
        post_link = reverse_lazy('payout_status')
        url = "https://api.freedompay.money/api/reg2nonreg"
        params = {
            'pg_amount': str(amount),
            'pg_order_id': str(order_id),
            'pg_description': description,
            'pg_post_link': str(post_link),
            'pg_back_link': self.pg_back_link,
            'pg_order_time_limit': order_time_limit
        }
        response = self.send_request(url, params, 'reg2nonreg')
        response_xml = ET.fromstring(response.content.decode())
        return response_xml

    def payout_to_saved_card(self, amount, order_id, user_id, card_token_to, description):
        """
        Осуществляет выплату на сохраненную карту.

        :param amount: Сумма выплаты.
        :param order_id: ID выплаты.
        :param user_id: ID пользователя.
        :param card_token_to: Токен карты получателя.
        :param description: Описание выплаты.
        """
        order_time_limit = timezone.now() + timedelta(days=1)
        order_time_limit = order_time_limit.strftime('%Y-%m-%d %H:%M:%S')
        post_link = reverse_lazy('payout_status')
        url = "https://api.freedompay.money/api/reg2reg"
        params = {
            'pg_amount': str(amount),
            'pg_order_id': str(order_id),
            'pg_user_id': str(user_id),
            'pg_card_token_to': card_token_to,
            'pg_description': description,
            'pg_post_link': post_link,
            'pg_back_link': self.pg_back_link,
            'pg_order_time_limit': order_time_limit
        }
        response = self.send_request(url, params, 'reg2reg')
        response_xml = ET.fromstring(response.content.decode())
        return response_xml

    def get_payment_status_by_order_id(self, order_id):
        """
        Получает статус платежа по его ID.

        :param order_id: ID платежа.
        :return: XML-ответ от платежной системы.
        """
        url = "https://api.paybox.money/get_status3.php"
        params = {
            'pg_order_id': order_id
        }
        response = self.send_request(url, params, 'get_status3.php')
        response_xml = ET.fromstring(response.content.decode())
        return response_xml