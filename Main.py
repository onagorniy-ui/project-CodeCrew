import pickle
from collections import UserDict
from datetime import datetime
from colorama import init, Fore, Style

# Ініціалізація colorama (autoreset=True автоматично скидає колір після кожного виводу)
init(autoreset=True)


# Базова обробка помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"{Fore.RED}ValueError: {e}"
        except KeyError as e:
            return f"{Fore.RED}KeyError: {e}"
        except IndexError:
            return f"{Fore.RED}IndexError: Not enough arguments."
        except Exception as e:
            return f"{Fore.RED}Error: {e}"
    return inner


# Класи для адресної книги
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


# Функції-обробники команд (Handlers)
@input_error
def add_contact(args, book: AddressBook):
    return f"{Fore.YELLOW}Функція add_contact ще не реалізована."

@input_error
def add_note(args, notebook: NoteBook):
    return f"{Fore.YELLOW}Функція add_note ще не реалізована."

# TODO: Додати інші обробники (change, phone, show_all, add_birthday, search, тощо)


# Збереження та завантаження даних
def save_data(book, notebook, filename="data.pkl"):
    # TODO: Реалізувати збереження обох книг на диск
    pass

def load_data(filename="data.pkl"):
    # TODO: Реалізувати завантаження. Якщо файлу немає, повертати нові AddressBook та NoteBook
    return AddressBook(), NoteBook()

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Головний цикл програми
def main():
    book, notebook = load_data()
    print(f"{Fore.BLUE}Welcome to the assistant bot!")

    while True:
        user_input = input(f"{Style.BRIGHT}Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book, notebook)
            print(f"{Fore.GREEN}Good bye!")
            break
        
        elif command == "hello":
            print(f"{Fore.BLUE}How can I help you?")
            
        elif command == "add":
            print(add_contact(args, book))

        elif command == "add-note":
            print(add_note(args, notebook))
            
        # TODO: Додати гілки elif для всіх інших команд
        # TODO: Додати сюди "Інтелектуальний аналіз" (вгадування команди)

        else:
            print(f"{Fore.RED}Invalid command.")

if __name__ == "__main__":
    main()