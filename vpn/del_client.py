import requests
import json


class X3:
    def __init__(self, login, password, host):
        self.login = login
        self.password = password
        self.host = host
        self.data = {"username": self.login, "password": self.password}
        self.ses = requests.Session()

    # Тестовое соединение (аутентификация)
    def test_connect(self):
        response = self.ses.post(f"{self.host}/login", data=self.data)
        if response.status_code == 200:
            print("Успешное подключение.")
            return True
        else:
            print("Ошибка подключения:", response.status_code, response.text)
            return False

    # Получение информации о клиентах для указанного inbound
    def list_clients(self, inbound_id):
        url = f"{self.host}/panel/api/inbounds/get/{inbound_id}"
        response = self.ses.get(url)
        if response.status_code == 200:
            inbound_info = response.json()
            # Извлекаем список клиентов из settings -> clients
            clients = json.loads(inbound_info["obj"]["settings"])["clients"]
            return clients
        else:
            print("Ошибка при получении информации об inbound:", response.status_code, response.text)
            return None

    # Удаление клиента из inbound
    def delete_client_from_inbound(self, inbound_id, client_id):
        url = f"{self.host}/panel/api/inbounds/{inbound_id}/delClient/{client_id}"

        headers = {
            "Accept": "application/json"
        }

        response = self.ses.post(url, headers=headers)

        if response.status_code == 200:
            print("Клиент успешно удалён:", response.json())
        else:
            print(f"Ошибка при удалении клиента: {response.status_code}, {response.text}")

def delete_client(email):
    # Конфигурация с вашими данными
    login = "LULfG1nGGh"
    password = "cJ9rltY7O1"
    host = "http://194.87.55.42:31896/mWeszy2ysXhmHdC"  # Access URL
    inbound_id = 1  # ID inbound, для которого нужно получить список клиентов

    # Создание экземпляра класса и выполнение операций
    x3_instance = X3(login, password, host)

    if x3_instance.test_connect():  # Попытка аутентификации
        # Запрашиваем email клиента, которого нужно удалить
        email_to_delete = email

        # Получаем список клиентов
        clients = x3_instance.list_clients(inbound_id)

        if clients:
            # Ищем клиента по email
            client_to_delete = None
            for client in clients:
                if client["email"] == email_to_delete:
                    client_to_delete = client
                    break

            # Удаляем клиента, если найден
            if client_to_delete:
                client_id = client_to_delete["id"]
                print(f"Найден клиент с email {email_to_delete}. Удаляем клиента с ID: {client_id}")
                x3_instance.delete_client_from_inbound(inbound_id, client_id)
            else:
                print(f"Клиент с email {email_to_delete} не найден.")

def del_all_clients():
    # Конфигурация с вашими данными
    login = "LULfG1nGGh"
    password = "cJ9rltY7O1"
    host = "http://194.87.55.42:31896/mWeszy2ysXhmHdC"  # Access URL
    inbound_id = 1  # ID inbound, для которого нужно получить список клиентов

    # Создание экземпляра класса и выполнение операций
    x3_instance = X3(login, password, host)

    if x3_instance.test_connect():  # Попытка аутентификации
        # Запрашиваем email клиента, которого нужно удалить

        # Получаем список клиентов
        clients = x3_instance.list_clients(inbound_id)

        if clients:
            for client in clients:
                if client["email"] != "TesTingClllll123ent@gm.com" and client["email"] != "TesTingClllll123ent@gmail.com":
                    x3_instance.delete_client_from_inbound(inbound_id, client["id"])


