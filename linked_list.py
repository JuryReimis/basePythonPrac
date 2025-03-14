from typing import Optional


class ObjList:
    def __init__(self, data: str, next_: Optional['ObjList'] = None, prev: Optional['ObjList'] = None):
        self.__next = next_
        self.__prev = prev
        self.__data = data

    def get_next(self) -> Optional['ObjList']:
        r"""Возвращает следующий элемент списка"""
        return self.__next

    def set_next(self, obj: Optional['ObjList']):
        r"""Устанавливает следующий элемент списка"""
        self.__next = obj

    def get_prev(self) -> Optional['ObjList']:
        r"""Возвращает предыдущий элемент списка"""
        return self.__prev

    def set_prev(self, obj: Optional['ObjList']):
        r"""Устанавливает предыдущий элемент списка"""
        self.__prev = obj

    def get_data(self) -> str:
        r"""Возвращает данные элемента списка"""
        return self.__data

    def set_data(self, data: str):
        r"""Устанавливает данные для элемента списка"""
        self.__data = data


class LinkedList:
    def __init__(self):
        self.head: ObjList | None = None
        self.tail: ObjList | None = None

    def add_obj(self, obj: ObjList):
        r"""Добавляет элемент в список"""
        if self.head is None:
            self.head = obj
            self.tail = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
            self.tail = obj

    def remove_obj(self):
        r"""Удаляет последний элемент из списка"""
        if self.tail is None:
            print("Список пуст, удаление невозможно!")
            return
        if self.tail.get_prev() is not None:
            pre_tail_obj = self.tail.get_prev()
            pre_tail_obj.set_next(None)
            self.tail = pre_tail_obj
        else:
            self.tail = self.head = None

    def get_data(self) -> list[str]:
        r"""Выводит список всей полезной нагрузки всех элементов списка"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.get_data())
            current = current.get_next()
        return result
