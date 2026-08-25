from collections import UserDict
from datetime import datetime


# Базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        # TODO: Додати валідацію номера телефону (10 цифр)
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        # TODO: Додати валідацію email
        super().__init__(value)


class Address(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        # TODO: Додати валідацію дати (DD.MM.YYYY)
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        # TODO: Реалізувати додавання телефону
        pass

    def edit_phone(self, old_phone, new_phone):
        # TODO: Реалізувати редагування телефону
        pass

    def add_birthday(self, birthday):
        # TODO: Реалізувати додавання дня народження
        pass

    # TODO: Додати методи для email та адреси


class AddressBook(UserDict):
    def add_record(self, record):
        # TODO: Реалізувати додавання запису (не забудьте про lower() для ключів)
        pass

    def find(self, name):
        # TODO: Реалізувати пошук
        pass

    def delete(self, name):
        # TODO: Реалізувати видалення
        pass

    def get_upcoming_birthdays(self, days):
        # TODO: Реалізувати пошук днів народження через задану кількість днів
        pass


# Класи для нотаток (Новий функціонал)
class Note:
    # TODO: Реалізувати клас нотатки (текст, теги)
    pass


class NoteBook(UserDict):
    # TODO: Реалізувати збереження, пошук, редагування нотаток
    pass
