from colorama import Fore, Style, init
from handlers import add_contact, add_note
from storage import load_data, save_data

# Ініціалізація colorama (autoreset=True автоматично скидає колір після кожного виводу)
init(autoreset=True)


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


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
