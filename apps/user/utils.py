from datetime import datetime
import string
import random
import requests
import xmltodict
from dicttoxml import dicttoxml
from django.conf import settings
from uuid import uuid4
from .models import CustomUser


class SendSMS:
    """
    A class for sending SMS messages using an API.
    """

    __url = 'http://smspro.nikita.kg/api/message'

    __headers = {'Content-Type': 'application/xml'}

    __xml = '<?xml version="1.0" encoding="UTF-8"?>' \
        '<message>' \
        '<login>{login}</login>' \
        '<pwd>{password}</pwd>' \
        '<id>{id}</id>' \
        '<sender>{sender}</sender>' \
        '<text>{text}</text>' \
        '<phones>{phones}</phones>' \
        '</message>' \


    def __init__(self, phone, text):
        """
        Initialize the SMS message with the recipient's phone number and the message text.
       Args:
           phone (str or list of str): The recipient's phone number(s).
           text (str): The message text to be sent.
        """
        if type(phone) not in (list, tuple):
            self.phone = [phone]
        else:
            self.phone = phone
        self.text = text

    def __get_phones(self):
        """
        Format the phone number(s) for the SMS API.
        Returns:
            str: A formatted string of phone numbers for the API.
        """
        phones = ''
        for phone in self.phone:
            phones += f'<phone>{phone}</phone>'
        return phones

    def __get_xml(self):
        xml = self.__xml.format(
            login="login",
            password="password",
            id=self.__get_id(),
            sender="sender",
            text=f'Use {self.text} to verify your  account.',
            phones=self.__get_phones()
            )
        return xml

    def __get_id(self):
        id = str(uuid4())[:10]
        return id

    @property
    def send(self):
        response = requests.post(
            url=self.__url,
            data=self.__get_xml(),
            headers=self.__headers
        )
        response_dict = xmltodict.parse(response.text)
        status = response_dict['response']['status']
        return status

    @staticmethod
    def set_verification_code(length=4):
        """
        Генерирует случайный код подтверждения указанной длины.
        """
        characters = string.digits
        verification_code = ''.join(random.choice(characters) for _ in range(length))
        return verification_code

    @classmethod
    def send_confirmation_sms(cls, user_obj: CustomUser) -> bool:
        """ Method for sending confirmation sms to a new or old user """
        verification_code = cls.set_verification_code()
        id_string = '%s%d' % (user_obj.id, datetime.now().timestamp())
        data = {
            'login': settings.NIKITA_LOGIN,
            'pwd': settings.NIKITA_PASSWORD,
            'id': id_string,
            'sender': 'SMSPRO.KG',
            'text': f'Ваш код активации:  {verification_code}',
            'phones': [str(user_obj.phone_number).replace('+', '')],
            # 'test': 1
        }
        page = dicttoxml(data, custom_root='message',
                         item_func=lambda x: x[:-1], attr_type=False)
        response = requests.post(
            url=cls.__url,
            data=page, headers=cls.__headers
        )
        response_dict = xmltodict.parse(response.text)
        print(response_dict)
        status = response_dict['response']['status']
        SendSMS(user_obj.name, verification_code).send
        user_obj.verification_code = verification_code
        user_obj.save()
        return True if status in ('0', '11') else False
