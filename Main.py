#імпортуємо класи, функції та методи з інших файлів
import os
from colorama import Fore, Style, init
from commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    add_note,
    change_phone,
    delete_contact,
    show_all_contacts,
    show_birthday,
    show_birthdays,
    show_help,
    show_phone,
)
from storage import load_data, save_data

#ініціалізація colorama (autoreset=True автоматично скидає колір після кожного виводу)
init(autoreset=True)

#функція розбору введеного тексту
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

#основна функція
def main():
    filename = "data.pkl" #ім'я файлу
    book, notebook = load_data(filename) #завантажуємо дані

    # перевіряємо чи файл існує, якщо ні то виводимо базове привітання
    if not os.path.exists(filename):
        print(f"{Fore.BLUE}Вітаю! Я NORA - ваш персональний помічник рекрутера.\nЯ допоможу з організацією контактів кандидатів\nі нотаток після комунікації")
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

        # todo: додати інші команди для нотаток (add-tag, find-note, sort-notes тощо)
        # todo: додати сюди "інтелектуальний аналіз" (вгадування команди)

        else:  # якщо команда не є жодною з вищезазначених
            print(f"{Fore.RED}Невірна команда, введіть 'help' для перегляду списку доступних команд.{Fore.RESET}")


if __name__ == "__main__":
    main()
