from typing import List, Set


class Server:
    last_ip = 0

    def __new__(cls, *args, **kwargs):
        r"""При создании нового экземпляра класса - он получает новый уникальный ip"""
        cls.last_ip += 1
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        self.ip = self.last_ip
        self.buffer: List[Data] = []
        self.linked_router: Set[Router] = set()

    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        if isinstance(other, Server):
            return self.ip == other.ip
        return False

    def send_data(self, data: 'Data'):
        r"""Отправка данных во все подключенные роутеры"""
        for router in self.linked_router:
            router.receive_data(data)

    def receive_data(self, data: 'Data'):
        r"""Метод принимает данные от роутера и записывает их в буфер"""
        self.buffer.append(data)

    def get_data(self) -> List['Data']:
        r"""Метод возвращает список принятых данных и очищает буфер"""
        buffer = list(self.buffer)
        self.buffer.clear()
        return buffer

    def get_ip(self) -> int:
        r"""Возвращает ip адрес сервера"""
        return self.ip

    def connect_new_router(self, router: 'Router'):
        self.linked_router.add(router)

    def disconnect_router(self, router: 'Router'):
        self.linked_router.remove(router)


class Router:
    last_ip = 0

    def __new__(cls, *args, **kwargs):
        cls.last_ip += 1
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        self.buffer: List[Data] = []
        self.ip = self.last_ip
        self.linked_servers: Set[Server] = set()

    def __hash__(self):
        return hash(self.ip)

    def __eq__(self, other):
        if isinstance(other, Router):
            return self.ip == other.ip
        return False

    def link(self, server: Server):
        r"""Метод подключает роутер к серверу"""
        server.connect_new_router(self)
        self.linked_servers.add(server)

    def unlink(self, server: Server):
        r"""Метод отключает роутер от сервера"""
        server.disconnect_router(self)
        self.linked_servers.remove(server)

    def send_data(self):
        r"""Метод для отправки всех пакетов данных на определенные сервера"""
        for data in self.buffer:
            for server in self.linked_servers:
                if data.target_ip == server.get_ip():
                    server.receive_data(data)
                    break
        self.buffer.clear()

    def receive_data(self, data: 'Data'):
        r"""Получение пакета от сервера и запись в буфер роутера"""
        self.buffer.append(data)


class Data:
    def __init__(self, data: str, target_ip):
        self.data = data
        self.target_ip = target_ip
