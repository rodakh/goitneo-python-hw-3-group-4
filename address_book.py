from collections import UserDict
from datetime import datetime, date, timedelta
import pickle


def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not str(value).isdigit() or len(str(value)) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid birthday format. Expected 'dd.mm.yyyy'.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                break

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = date.today()
        one_week_later = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                bday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                bday_this_year = date(today.year, bday_date.month, bday_date.day)
                if not is_leap(today.year) and bday_this_year.month == 2 and bday_this_year.day == 29:
                    bday_this_year = bday_this_year.replace(day=28)

                if today <= bday_this_year <= one_week_later:
                    upcoming_birthdays.append(record.name.value)

        return upcoming_birthdays

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(dict(self), file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            loaded_data = pickle.load(file)
            self.data.update(loaded_data)
