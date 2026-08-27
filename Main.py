# імпортуємо бібліотеки, класи та функції
import difflib
import os

try:
    import readline  # підтримка історії команд через стрілки
except ImportError:
    pass  # якщо бібліотека недоступна, програма продовжить працювати


from colorama import Fore, Style, init
from commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    add_note,
    add_tag,
    change_phone,
    delete_contact,
    delete_note,
    edit_note,
    find_note,
    find_tag,
    search_contacts,
    show_all_contacts,
    show_all_notes,
    show_birthday,
    show_birthdays,
    show_help,
    show_phone,
    sort_notes,
)
from storage import load_data, save_data

# ініціалізація colorama (autoreset=True автоматично скидає колір після кожного виводу)
init(autoreset=True)

# список усіх відомих команд для інтелектуального аналізу (автопідказки)
ALL_COMMANDS = [
    "hello",
    "help",
    "close",
    "exit",
    "add",
    "change",
    "phone",
    "all",
    "all-contacts",
    "search",
    "search-contacts",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-email",
    "add-address",
    "delete-contact",
    "add-note",
    "edit-note",
    "delete-note",
    "add-tag",
    "find-note",
    "find-tag",
    "search-by-tag",
    "sort-notes",
    "all-notes",
    "show-notes",
]


# функція інтелектуального пошуку найбільш схожої команди
def suggest_command(command: str) -> str | None:
    matches = difflib.get_close_matches(command, ALL_COMMANDS, n=1, cutoff=0.6)
    return matches[0] if matches else None


# функція розбору введеного тексту
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# основна функція
def main():
    filename = "data.pkl"  # ім'я файлу
    book, notebook = load_data(filename)  # завантажуємо дані

    # перевіряємо чи файл існує, якщо ні то виводимо базове привітання
    if not os.path.exists(filename):
        print(
            f"{Fore.BLUE}Вітаю! Я NORA - ваш персональний помічник рекрутера.\n"
            f"Я допоможу з організацією контактів кандидатів\n"
            f"і нотаток після комунікації"
        )
    # перевіряємо чи словники порожні, якщо порожні то виводимо скорочене привітання
    elif not book.data and not notebook.data:
        print(f"{Fore.BLUE}Я NORA і я рада знову вітати вас!\nВаші дані були завантажені, {Fore.YELLOW}але вони порожні.")
    # якщо файл існує і дані не порожні то виводимо скорочене привітання
    else:
        print(f"{Fore.BLUE}Я NORA і я рада знову вітати вас!\nВаші дані були успішно завантажені.")

    # відображаємо при першому запуску список доступних команд
    print(show_help())

    while True:
        user_input = input("Введіть команду: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book, notebook)
            print(f"{Fore.BLUE}До побачення!")
            break

        elif command == "hello":
            print(f"{Fore.BLUE}Чим можу допомогти?")

        elif command == "help":
            print(show_help())

        # команди для контактів
        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command in ["all", "all-contacts"]:
            print(show_all_contacts(book))

        elif command in ["search", "search-contacts"]:
            print(search_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_birthdays(args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "add-address":
            print(add_address(args, book))

        elif command == "delete-contact":
            print(delete_contact(args, book))

        # команди для нотаток
        elif command == "add-note":
            print(add_note(args, notebook))

        elif command == "edit-note":
            print(edit_note(args, notebook))

        elif command == "delete-note":
            print(delete_note(args, notebook))

        elif command == "add-tag":
            print(add_tag(args, notebook))

        elif command == "find-note":
            print(find_note(args, notebook))

        elif command in ["find-tag", "search-by-tag"]:
            print(find_tag(args, notebook))

        elif command == "sort-notes":
            print(sort_notes(notebook))

        elif command in ["all-notes", "show-notes"]:
            print(show_all_notes(notebook))

        # якщо команда не розпізнана - інтелектуальна автопідказка
        else:
            suggestion = suggest_command(command)
            if suggestion:
                print(
                    f"{Fore.YELLOW}Невідома команда '{command}'. "
                    f"Можливо, ви мали на увазі: {Fore.GREEN}{suggestion}{Fore.YELLOW}?\n"
                    f"{Fore.YELLOW}Введіть 'help' для перегляду списку всіх команд."
                )
            else:
                print(f"{Fore.RED}Невірна команда. Введіть 'help' для перегляду списку доступних команд.")


if __name__ == "__main__":
    main()
