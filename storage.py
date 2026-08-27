import pickle

from classes import AddressBook, NoteBook


def save_data(book, notebook, filename="data.pkl"):
    """Зберігає книгу контактів і книгу нотаток у файл."""
    data = {
        "book": book,
        "notebook": notebook,
    }

    with open(filename, "wb") as file:
        pickle.dump(data, file)


def load_data(filename="data.pkl"):
    """Завантажує дані або повертає нові порожні книги."""
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)

        return data["book"], data["notebook"]

    except (
        FileNotFoundError,
        EOFError,
        pickle.UnpicklingError,
    ):
        return AddressBook(), NoteBook()