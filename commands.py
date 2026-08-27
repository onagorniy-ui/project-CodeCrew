from colorama import Fore
from classes import AddressBook, Note, NoteBook, Record


# декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"{Fore.RED}{e}"
        except KeyError as e:
            return f"{Fore.RED}{e}"
        except IndexError:
            return f"{Fore.RED}Не вистачає аргументів для команди."
        except Exception as e:
            return f"{Fore.RED}{e}"

    return inner


# функція show_help - вивід списку доступних команд
def show_help():
    return f"""{Fore.BLUE}
Ось список доступних команд:

Контакти:
hello - привітання
help - показати це повідомлення
add [name] [phone] - додати новий контакт або додати номер до контакту
change [name] [old_phone] [new_phone] - змінити номер телефону контакту
phone [name] - показати номер телефону контакту
all - показати всі контакти
search [запит] - знайти контакти за ім'ям, телефоном, email або адресою
add-birthday [name] [birthday] - додати день народження контакту (DD.MM.YYYY)
show-birthday [name] - показати день народження контакту
birthdays [days] - показати найближчі дні народження (за замовчуванням: 7 днів)
add-email [name] [email] - додати email контакту
add-address [name] [address] - додати адресу контакту
delete-contact [name] - видалити контакт

Нотатки:
add-note [title] [text] - створити нову нотатку
edit-note [title] [new_text] - змінити текст нотатки
delete-note [title] - видалити нотатку
add-tag [title] #[tag] - додати тег до нотатки (наприклад: add-tag Python #backend)
find-note [text] - знайти нотатки за текстом
#[tag], find-tag [tag] - пошук нотаток за тегом (наприклад: #dev або find-tag python)
sort-notes - показати нотатки, посортовані за тегами
all-notes - показати всі збережені нотатки

Завершення:
close, exit - завершити роботу та зберегти дані
"""


# функції-обробники команд для контактів

# функція додавання контакту
@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Вкажіть ім'я та номер телефону (наприклад: add Oleg 0991234567).")
    name, phone = args[0], args[1]
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f"{Fore.BLUE}Контакт {name} успішно створено з номером {phone}."
    else:
        record.add_phone(phone)
        return f"{Fore.BLUE}До контакту {name} додано додатковий номер {phone}."


# функція зміни номера телефону
@input_error
def change_phone(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Вкажіть ім'я, старий номер та новий номер (наприклад: change Oleg 0991234567 0671112233).")
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт {name} не знайдено.")
    record.edit_phone(old_phone, new_phone)
    return f"{Fore.BLUE}Номер {old_phone} контакту {name} змінено на {new_phone}."


# функція показу телефону
@input_error
def show_phone(args, book: AddressBook):
    if not args:
        raise ValueError("Вкажіть ім'я контакту (наприклад: phone Oleg).")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт {name} не знайдено.")
    phones = ", ".join(p.value for p in record.phones) if record.phones else "немає"
    return f"{Fore.BLUE}{record.name.value}: {phones}"


# функція показу всіх контактів
@input_error
def show_all_contacts(book: AddressBook):
    if not book.data:
        return f"{Fore.YELLOW}Книга контактів порожня."
    return f"{Fore.BLUE}" + "\n".join(str(record) for record in book.data.values())


# функція додавання дня народження
@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Вкажіть ім'я та дату народження (наприклад: add-birthday Oleg 28.08.1995).")
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт {name} не знайдено.")
    record.add_birthday(birthday)
    return f"{Fore.BLUE}День народження {birthday} додано для {record.name.value}."


# функція показу дня народження
@input_error
def show_birthday(args, book: AddressBook):
    if not args:
        raise ValueError("Вкажіть ім'я контакту (наприклад: show-birthday Oleg).")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт {name} не знайдено.")
    if record.birthday is None:
        return f"{Fore.YELLOW}Для контакту {record.name.value} день народження не вказано."
    return f"{Fore.BLUE}{record.name.value}: {record.birthday.value}"


# функція показу днів народження
@input_error
def show_birthdays(args, book: AddressBook):
    if args:
        if not args[0].isdigit():
            raise ValueError("Кількість днів має бути додатним числом (наприклад: birthdays 7).")
        days = int(args[0])
    else:
        days = 7

    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"{Fore.YELLOW}У найближчі {days} днів іменинників немає."
    return f"{Fore.BLUE}" + "\n".join(f"{r.name.value}: {r.birthday.value}" for r in upcoming)


# функція додавання email
@input_error
def add_email(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Вкажіть ім'я та email (наприклад: add-email Oleg test@gmail.com).")
    name, email = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт {name} не знайдено.")
    record.add_email(email)
    return f"{Fore.BLUE}Email {email} додано для {record.name.value}."


# функція додавання адреси
@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Вкажіть ім'я та адресу (наприклад: add-address Oleg Київ, Хрещатик 1).")
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт {name} не знайдено.")
    record.add_address(address)
    return f"{Fore.BLUE}Адресу '{address}' додано для {record.name.value}."


# функція видалення контакту
@input_error
def delete_contact(args, book: AddressBook):
    if not args:
        raise ValueError("Вкажіть ім'я контакту (наприклад: delete-contact Oleg).")
    name = args[0]
    book.delete(name)
    return f"{Fore.BLUE}Контакт {name} успішно видалено."


# функція пошуку контактів за підрядком
@input_error
def search_contacts(args, book: AddressBook):
    if not args:
        raise ValueError("Вкажіть запит для пошуку (наприклад: search Oleg або search 099).")
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return f"{Fore.YELLOW}За запитом '{query}' контактів не знайдено."
    return f"{Fore.BLUE}" + "\n".join(str(record) for record in results)


# функції-обробники команд для нотаток (завдання Ярослави Журіхіної)
# todo: реалізувати функції для нотаток (add_note, edit_note, delete_note, add_tag, find_note, find_tag, sort_notes, show_all_notes)


