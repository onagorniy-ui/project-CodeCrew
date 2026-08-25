import pickle
from models import AddressBook, NoteBook


def save_data(book, notebook, filename="data.pkl"):
    """Реалізувати збереження обох книг на диск."""
    # TODO: Реалізувати збереження обох книг на диск
    pass


def load_data(filename="data.pkl"):
    """Реалізувати завантаження. Якщо файлу немає, повертати нові AddressBook та NoteBook."""
    # TODO: Реалізувати завантаження. Якщо файлу немає, повертати нові AddressBook та NoteBook
    return AddressBook(), NoteBook()
