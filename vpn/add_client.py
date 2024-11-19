import sys

sys.stdout.reconfigure(encoding='utf-8')

import requests
import json
import uuid  # Для генерации уникального идентификатора клиента
import urllib.parse  # Для кодирования tag в URL


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
            return True
        else:
            print("Ошибка подключения:", response.status_code, response.text)
            return False

    # Получение текущих настроек inbound
    def get_inbound_settings(self, inbound_id):
        url = f"{self.host}/panel/api/inbounds/get/{inbound_id}"
        response = self.ses.get(url)
        if response.status_code == 200:
            inbound_info = response.json()
            return inbound_info["obj"]  # Возвращаем настройки inbound
        else:
            print("Ошибка при получении настроек inbound:", response.status_code, response.text)
            return None

    # Добавление нового клиента к inbound
    def add_client_to_inbound(self, inbound_id, new_client_settings):
        url = f"{self.host}/panel/api/inbounds/addClient"

        payload = {
            "id": inbound_id,
            "settings": json.dumps(new_client_settings)  # Преобразуем настройки клиента в строку JSON
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = self.ses.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return new_client_settings["clients"][0]["id"]  # Возвращаем UUID клиента
        else:
            print("Ошибка при добавлении клиента:", response.status_code, response.text)
            return None


def connect(email):
    # Конфигурация с вашими данными
    login = "LULfG1nGGh"
    password = "cJ9rltY7O1"
    host = "http://194.87.55.42:31896/mWeszy2ysXhmHdC"  # Access URL

    # ID inbound, для которого добавляется клиент
    inbound_id = 1
    default_server_address = "194.87.55.42"  # IP-адрес сервера по умолчанию

    # Создание экземпляра класса
    x3_instance = X3(login, password, host)

    # Выполнение операций
    if x3_instance.test_connect():  # Попытка аутентификации
        inbound_settings = x3_instance.get_inbound_settings(inbound_id)

        if inbound_settings:
            # Запрашиваем email нового клиента
            new_client_email = email

            # Создаём нового клиента
            new_client_id = str(uuid.uuid4())  # Генерируем уникальный ID

            new_client_settings = {
                "clients": [
                    {
                        "id": new_client_id,
                        "email": new_client_email,
                        "enable": True,
                        "expiryTime": 0,
                        "flow": "",
                        "limitIp": 0,
                        "totalGB": 0,
                        "tgId": "",
                        "subId": "unique-sub-id",  # Можно создать уникальный ID или использовать любое значение
                        "reset": 0
                    }
                ]
            }

            client_key = x3_instance.add_client_to_inbound(inbound_id, new_client_settings)

            if client_key:
                # Извлекаем настройки для подключения
                stream_settings = json.loads(inbound_settings["streamSettings"])
                security = stream_settings.get("security", "none")
                reality_settings = stream_settings.get("realitySettings", {})
                reality_settings_details = reality_settings.get("settings", {})

                # Извлечение параметров reality
                pbk = reality_settings_details.get("publicKey", "")
                fp = reality_settings_details.get("fingerprint", "chrome")
                sni = reality_settings.get("serverNames", [""])[0]  # Берём первый сервер из списка
                sid = reality_settings.get("shortIds", [""])[0]  # Берём первый shortId
                spx = reality_settings_details.get("spiderX", "")

                # Формируем строку подключения
                server_address = inbound_settings.get("listen") or default_server_address  # Используем IP по умолчанию
                port = inbound_settings["port"]
                type_connection = stream_settings.get("network", "tcp")

                encoded_tag = urllib.parse.quote(f"test1-{new_client_email}")

                connection_string = (
                    f"vless://{client_key}@{server_address}:{port}"
                    f"?type={type_connection}&security={security}"
                )

                if security == "reality":
                    connection_string += (
                        f"&pbk={pbk}&fp={fp}&sni={sni}&sid={sid}&spx={urllib.parse.quote(spx)}"
                    )

                connection_string += f"#{encoded_tag}"

                print("\nСтрока подключения для клиента:")
                print(connection_string)
                return connection_string
            else:
                print("Не удалось создать клиента.")
        else:
            print("Ошибка: не удалось получить настройки inbound.")