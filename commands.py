from colorama import Fore
from classes import AddressBook, NoteBook


# декоратор для обробки помилок введення
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


# функції-обробники команд
@input_error
def add_contact(args, book: AddressBook):
    return f"{Fore.YELLOW}Функція add_contact ще не реалізована."


@input_error
def add_note(args, notebook: NoteBook):
    return f"{Fore.YELLOW}Функція add_note ще не реалізована."


# todo: додати інші обробники (change, phone, show_all, add_birthday, search, тощо)
