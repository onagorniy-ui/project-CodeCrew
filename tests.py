import os
import tempfile
import pickle
import unittest
from datetime import datetime, timedelta

from classes import AddressBook, Record, Name, Phone, Email, Address, Birthday, NoteBook, Note
from storage import save_data, load_data
from Main import suggest_command, parse_input
from commands import (
    add_contact, change_phone, show_phone, show_all_contacts,
    add_birthday, show_birthday, show_birthdays,
    add_email, add_address, delete_contact, search_contacts,
    add_note, edit_note, delete_note, add_tag, find_note, find_tag, sort_notes, show_all_notes
)


class TestAddressBookAndRecord(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_phone_validation(self):
        # Валідний номер з 10 цифр
        phone = Phone("0991234567")
        self.assertEqual(phone.value, "0991234567")

        # Невалідний номер (менше/більше 10 цифр або з літерами)
        with self.assertRaises(ValueError):
            Phone("12345")
        with self.assertRaises(ValueError):
            Phone("099123456789")
        with self.assertRaises(ValueError):
            Phone("099123456a")

    def test_email_validation(self):
        # Валідний email
        email = Email("test@domain.com")
        self.assertEqual(email.value, "test@domain.com")

        # Невалідний email
        with self.assertRaises(ValueError):
            Email("test_no_at.com")
        with self.assertRaises(ValueError):
            Email("test@nodomain")

    def test_birthday_validation_and_upcoming(self):
        # Валідний день народження
        bday = Birthday("28.08.1995")
        self.assertEqual(bday.value, "28.08.1995")

        # Невалідний формат
        with self.assertRaises(ValueError):
            Birthday("1995-08-28")
        with self.assertRaises(ValueError):
            Birthday("32.13.2024")

        # Перевірка найближчих днів народження
        rec = Record("Oleg")
        target_date = (datetime.today() + timedelta(days=3)).strftime("%d.%m.%Y")
        rec.add_birthday(target_date)
        self.book.add_record(rec)

        upcoming = self.book.get_upcoming_birthdays(7)
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0].name.value, "Oleg")

    def test_contact_search_substring(self):
        rec = Record("Anastasia")
        rec.add_phone("0991112233")
        rec.add_email("hr@company.ua")
        rec.add_address("Kyiv, Khreshchatyk")
        self.book.add_record(rec)

        # Пошук за ім'ям
        self.assertEqual(len(self.book.search("anast")), 1)
        # Пошук за номером
        self.assertEqual(len(self.book.search("11122")), 1)
        # Пошук за поштою
        self.assertEqual(len(self.book.search("company")), 1)
        # Пошук за адресою
        self.assertEqual(len(self.book.search("Khreshchatyk")), 1)
        # Пошук неіснуючого
        self.assertEqual(len(self.book.search("Nonexistent")), 0)


class TestNoteBookAndNotes(unittest.TestCase):
    def setUp(self):
        self.nb = NoteBook()

    def test_notes_crud_and_keywords(self):
        # Додавання
        note = Note("PythonLead", "Needs FastAPI and Docker experience")
        self.nb.add_note(note)
        self.assertIn("PythonLead", self.nb.data)

        # Пошук за ключовими словами
        found = self.nb.find_note("FastAPI")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].title, "PythonLead")

        # Редагування
        self.nb.edit_note("PythonLead", "Updated: FastAPI v2")
        self.assertEqual(self.nb.data["PythonLead"].text, "Updated: FastAPI v2")

        # Видалення
        self.nb.delete_note("PythonLead")
        self.assertNotIn("PythonLead", self.nb.data)

    def test_tag_handling_and_sorting(self):
        note1 = Note("BackendDev", "Python developer")
        note1.add_tag("#python")
        note1.add_tag("#backend")
        self.nb.add_note(note1)

        note2 = Note("Designer", "UI/UX Figma designer")
        note2.add_tag("#design")
        self.nb.add_note(note2)

        # Пошук за тегом (з # та без #)
        self.assertEqual(len(self.nb.search_by_tag("#python")), 1)
        self.assertEqual(len(self.nb.search_by_tag("backend")), 1)
        self.assertEqual(len(self.nb.search_by_tag("#PYTHON")), 1)

        # Сортування за тегами
        sorted_notes = self.nb.sort_by_tag()
        self.assertEqual(len(sorted_notes), 2)


class TestStorage(unittest.TestCase):
    def setUp(self):
        temp = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file = temp.name
        temp.close()
        self.book = AddressBook()
        self.book.add_record(Record("Oleg"))
        self.nb = NoteBook()
        self.nb.add_note(Note("TestNote", "Test text"))

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_and_load(self):
        save_data(self.book, self.nb, self.temp_file)
        loaded_book, loaded_nb = load_data(self.temp_file)
        self.assertIn("oleg", loaded_book.data)
        self.assertIn("TestNote", loaded_nb.data)

    def test_corrupted_and_empty_file_recovery(self):
        # Пошкоджений файл
        with open(self.temp_file, "wb") as f:
            f.write(b"NOT_PICKLE_DATA")
        b_corrupt, nb_corrupt = load_data(self.temp_file)
        self.assertIsInstance(b_corrupt, AddressBook)
        self.assertIsInstance(nb_corrupt, NoteBook)

        # Порожній файл
        with open(self.temp_file, "wb") as f:
            pass
        b_empty, nb_empty = load_data(self.temp_file)
        self.assertIsInstance(b_empty, AddressBook)
        self.assertIsInstance(nb_empty, NoteBook)

    def test_backward_compatibility(self):
        # Збереження старим кортежем
        with open(self.temp_file, "wb") as f:
            pickle.dump((self.book, self.nb), f)
        b_tup, nb_tup = load_data(self.temp_file)
        self.assertIn("oleg", b_tup.data)

        # Збереження лише однією AddressBook
        with open(self.temp_file, "wb") as f:
            pickle.dump(self.book, f)
        b_single, nb_single = load_data(self.temp_file)
        self.assertIn("oleg", b_single.data)
        self.assertIsInstance(nb_single, NoteBook)


class TestCLIAndSuggestions(unittest.TestCase):
    def test_suggestions(self):
        self.assertEqual(suggest_command("ad"), "add")
        self.assertEqual(suggest_command("phoen"), "phone")
        self.assertEqual(suggest_command("birtday"), "birthdays")
        self.assertEqual(suggest_command("find-not"), "find-note")

    def test_parse_input(self):
        cmd, *args = parse_input("add Oleg 0991234567")
        self.assertEqual(cmd, "add")
        self.assertEqual(args, ["Oleg", "0991234567"])


if __name__ == "__main__":
    unittest.main()
