from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import UserDict
import pickle


class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.is_valid_phone(new_value):
            self.__value = new_value

    def is_valid_phone(self, phone):
        return phone.isdigit()


class Birthday(Field):
    def __init__(self, birthday):
        self.value = None
        self.set_birthday(birthday)

    def set_birthday(self, birthday):
        if self.is_valid_birthday(birthday):
            self.value = birthday
        else:
            raise ValueError("Invalid birthday")

    def is_valid_birthday(self, birthday):
        return True


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phone.set_phone(phone)

    def remove_phone(self, phone):
        if self.phone.value == phone:
            self.phone.value = None

    def edit_phone(self, old_phone, new_phone):
        if self.phone.value == old_phone:
            self.phone.set_phone(new_phone)

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            next_birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record_name):
        if record_name in self.data:
            del self.data[record_name]

    def get_record(self, record_name):
        return self.data.get(record_name)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def search_by_phone(self, query):
        results = []
        for record in self.data.values():
            if record.phone.value and query in record.phone.value:
                results.append(record)
        return results

    def search_by_name(self, query):
        results = []
        for record in self.data.values():
            if record.name.value and query in record.name.value:
                results.append(record)
        return results


# Абстрактний клас для уявлень
class View(ABC):
    @abstractmethod
    def display_record(self, record):
        pass

    @abstractmethod
    def display_search_results(self, results):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def display_commands(self):
        pass


# Конкретний клас для консольного інтерфейсу
class ConsoleView(View):
    def display_record(self, record):
        print(
            f"Name: {record.name.value}, Phone: {record.phone.value}, Birthday: {record.birthday.value if record.birthday else 'N/A'}")

    def display_search_results(self, results):
        if results:
            for record in results:
                self.display_record(record)
        else:
            self.display_message("No results found.")

    def display_message(self, message):
        print(message)

    def display_commands(self):
        commands = """
Available commands:
1. add - Add a new contact
2. remove - Remove an existing contact
3. search - Search for a contact by name or phone
4. list - List all contacts
5. save - Save the address book to a file
6. load - Load the address book from a file
7. exit - Exit the program
"""
        print(commands)


# Тестовий код
if __name__ == "__main__":
    ab = AddressBook()
    view = ConsoleView()

    rec1 = Record('Bill', '1234567890', '1990-08-15')
    rec2 = Record('Alice', '9876543210', '1995-10-20')
    ab.add_record(rec1)
    ab.add_record(rec2)

    # Зберегти адресну книгу на диск
    ab.save_to_file('address_book.pickle')

    # Очистити адресну книгу з пам'яті
    del ab

    # Відновити адресну книгу з диска
    ab = AddressBook()
    ab.load_from_file('address_book.pickle')

    # Пошук за номером телефону
    phone_query = '123'
    phone_results = ab.search_by_phone(phone_query)
    view.display_search_results(phone_results)

    # Пошук за ім'ям
    name_query = 'Alice'
    name_results = ab.search_by_name(name_query)
    view.display_search_results(name_results)

    # Відображення команд
    view.display_commands()