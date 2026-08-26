from collections import UserDict
from datetime import datetime


# базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        # todo: додати валідацію номера телефону (10 цифр)
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        # todo: додати валідацію email
        super().__init__(value)


class Address(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        # todo: додати валідацію дати (DD.MM.YYYY)
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        # todo: реалізувати додавання телефону
        pass

    def edit_phone(self, old_phone, new_phone):
        # todo: реалізувати редагування телефону
        pass

    def add_birthday(self, birthday):
        # todo: реалізувати додавання дня народження
        pass

    # todo: додати методи для email та адреси


class AddressBook(UserDict):
    def add_record(self, record):
        # todo: реалізувати додавання запису (не забудьте про lower() для ключів)
        pass

    def find(self, name):
        # todo: реалізувати пошук
        pass

    def delete(self, name):
        # todo: реалізувати видалення
        pass

    def get_upcoming_birthdays(self, days):
        # todo: реалізувати пошук днів народження через задану кількість днів
        pass


# класи для нотаток (новий функціонал)
class Note:
    # todo: реалізувати клас нотатки (текст, теги)
    pass


class NoteBook(UserDict):
    # todo: реалізувати збереження, пошук, редагування нотаток
    pass
