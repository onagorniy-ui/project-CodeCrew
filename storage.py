import pickle

from classes import AddressBook, NoteBook


def save_data(book, notebook, filename="data.pkl"):
    """Зберігає книгу контактів і книгу нотаток у файл."""
    data = {
        "book": book,
        "notebook": notebook,
    }

    try:
        with open(filename, "wb") as file:
            pickle.dump(data, file)
    except Exception as e:
        print(f"Помилка при збереженні даних у файл '{filename}': {e}")


def load_data(filename="data.pkl"):
    """Завантажує дані або повертає нові порожні книги."""
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)

        if isinstance(data, dict):
            return data.get("book", AddressBook()), data.get("notebook", NoteBook())

        if isinstance(data, tuple) and len(data) == 2:
            return data[0], data[1]

        if isinstance(data, AddressBook):
            return data, NoteBook()

        return AddressBook(), NoteBook()

    except (
        FileNotFoundError,
        EOFError,
        pickle.UnpicklingError,
        Exception,
    ):
        return AddressBook(), NoteBook()