import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

# Путь к файлу конфигурации Firebase
cred = credentials.Certificate("C:/Users/LENOVO/PycharmProjects/TSJ/firebase_service_account.json")


# Инициализация приложения Firebase
firebase_admin.initialize_app(cred)


def send_notification(token, title, body):
    # Создание сообщения
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )

    # Отправка сообщения
    response = messaging.send(message)
    print("Successfully sent message:", response)
