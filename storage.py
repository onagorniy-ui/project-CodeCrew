import pickle
from classes import AddressBook, NoteBook


def save_data(book, notebook, filename="data.pkl"):
    """реалізувати збереження обох книг на диск."""
    # todo: реалізувати збереження обох книг на диск
    pass


def load_data(filename="data.pkl"):
    """реалізувати завантаження. якщо файлу немає, повертати нові AddressBook та NoteBook."""
    # todo: реалізувати завантаження. якщо файлу немає, повертати нові AddressBook та NoteBook та не забути реалізуівати обробку помилок
    return AddressBook(), NoteBook()

    # except (FileNotFoundError, pickle.UnpicklingError, EOFError): # обробка помилок: файл не знайдено, файл пошкоджено, файл порожній
    #     return AddressBook(), NoteBook()