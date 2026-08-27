from collections import UserDict
from datetime import datetime


# базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# поле для імені контакту
class Name(Field):
    pass


# поле для телефону з валідацією
class Phone(Field):
    def __init__(self, value):
        # номер має складатися рівно з 10 цифр
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Номер телефону має містити рівно 10 цифр.")
        super().__init__(value)


# поле для email з валідацією
class Email(Field):
    def __init__(self, value):
        # крапка перевіряється саме в частині після @, а не будь де в рядку
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Email має містити '@' та '.'.")
        super().__init__(value)


# поле для адреси
class Address(Field):
    pass


# поле для дня народження з валідацією
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Дата народження має бути у форматі DD.MM.YYYY.")
        super().__init__(value)


# запис одного контакту в книзі
class Record:
    def __init__(self, name):
        self.name = Name(name)  # ім'я зберігається в оригінальному регістрі
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for index, existing_phone in enumerate(self.phones):
            if existing_phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError(f"Телефон {old_phone} не знайдено.")

    def remove_phone(self, phone):
        for existing_phone in self.phones:
            if existing_phone.value == phone:
                self.phones.remove(existing_phone)
                return
        raise ValueError(f"Телефон {phone} не знайдено.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "немає"
        email = self.email.value if self.email else "немає"
        address = self.address.value if self.address else "немає"
        birthday = self.birthday.value if self.birthday else "немає"
        return f"Ім'я: {self.name.value}, Телефони: {phones}, Email: {email}, Адреса: {address}, День народження: {birthday}"



# книга контактів
class AddressBook(UserDict):
    def add_record(self, record):
        # ключем у словнику є ім'я в нижньому регістрі
        self.data[record.name.value.lower()] = record

    def find(self, name):
        return self.data.get(name.lower())

    def delete(self, name):
        key = name.lower()
        if key not in self.data:
            raise KeyError(f"Контакт {name} не знайдено.")
        del self.data[key]

    def get_upcoming_birthdays(self, days):
        upcoming = []
        today = datetime.today().date()

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            try:
                birthday_this_year = birthday_date.replace(year=today.year)
            except ValueError:
                # 29 лютого у невисокосному році, переносимо на 28 лютого
                birthday_this_year = birthday_date.replace(
                    year=today.year, day=28, month=2
                )

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # включає сьогодні і межу в days днів
            if 0 <= (birthday_this_year - today).days <= days:
                upcoming.append(record)

        return upcoming

    # пошук контактів за фрагментом тексту в імені, телефоні, email або адресі
    def search(self, query: str):
        q = query.lower().strip()
        results = []
        for record in self.data.values():
            if q in record.name.value.lower():  # збіг по імені
                results.append(record)
            elif any(q in p.value for p in record.phones):  # збіг по телефону
                results.append(record)
            elif record.email and q in record.email.value.lower():  # збіг по email
                results.append(record)
            elif record.address and q in record.address.value.lower():  # збіг по адресі
                results.append(record)
        return results


# одна нотатка з тегами
class Note:
    def __init__(self, title, text, tags=None):
        self.title = title
        self.text = text
        self.tags = set(tags) if tags else set()

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.discard(tag)

    def __str__(self):
        tags = ", ".join(f"#{t}" for t in sorted(self.tags)) if self.tags else "немає"  # теги як хештеги
        return f"Назва: {self.title}\nТекст: {self.text}\nТеги: {tags}"


# книга нотаток
class NoteBook(UserDict):
    def add_note(self, note):
        # ключем є title у оригінальному вигляді, без приведення регістру
        self.data[note.title] = note

    def find_note(self, keyword):
        return [
            note for note in self.data.values() if keyword.lower() in note.text.lower()
        ]

    def search_by_tag(self, tag):
        return [note for note in self.data.values() if tag in note.tags]

    def sort_by_tag(self):
        # сортування за списком тегів кожної нотатки в алфавітному порядку
        return sorted(self.data.values(), key=lambda note: sorted(note.tags))

    def edit_note(self, title, new_text):
        if title not in self.data:
            raise KeyError(f"Нотатку {title} не знайдено.")
        self.data[title].text = new_text

    def delete_note(self, title):
        if title not in self.data:
            raise KeyError(f"Нотатку {title} не знайдено.")
        del self.data[title]
