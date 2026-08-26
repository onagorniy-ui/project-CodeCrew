import os
from colorama import Fore, Style, init
from commands import add_contact, add_note, show_help
from storage import load_data, save_data

# ініціалізація colorama (autoreset=True автоматично скидає колір після кожного виводу)
init(autoreset=True)


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# ffff
def main():
    filename = "data.pkl"
    book, notebook = load_data(filename)

    # перевіряємо чи файл існує, якщо ні то виводимо базове привітання
    if not os.path.exists(filename):
        print(f"{Fore.BLUE}Welcome to the assistant bot!")
    # перевіряємо чи словники порожні, якщо порожні то виводимо привітання
    elif not book.data and not notebook.data:
        print(f"{Fore.BLUE}Welcome to the assistant bot!\nYour data was loaded, {Fore.YELLOW}but it is empty.")
    # якщо файл існує і дані не порожні то виводимо привітання
    else:
        print(f"{Fore.BLUE}Welcome to the assistant bot!\nYour data was loaded successfully.")

    # відображаємо список доступних команд
    print(f"{Fore.BLUE}Here is the list of available commands:{Fore.RESET}\n{show_help()}")

    while True:
        user_input = input(f"Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book, notebook)
            print(f"{Fore.BLUE}Good bye!")
            break

        elif command == "hello":
            print(f"{Fore.BLUE}How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "add-note":
            print(add_note(args, notebook))
        
        elif command == "help":
            print(f"{Fore.BLUE}{show_help()}{Fore.RESET}")

        # todo: додати гілки elif для всіх інших команд
        # todo: додати сюди "інтелектуальний аналіз" (вгадування команди)

        else:  # якщо команда не є жодною з вищезазначених
            print(f"{Fore.RED}Invalid command, type 'help'.{Fore.RESET}")


if __name__ == "__main__":
    main()
