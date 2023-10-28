from address_book import AddressBook, Record
import os


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Invalid input."
        except IndexError:
            return "Command not recognized."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(book, name, phone):
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
def change_contact(book, name, phone):
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, phone)
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(book, name):
    record = book.find(name)
    if record:
        return '; '.join(phone.value for phone in record.phones)
    else:
        raise KeyError


@input_error
def show_all(book):
    return "\n".join([str(record) for record in book.data.values()])


@input_error
def add_birthday(book, name, bday):
    record = book.find(name)
    if record:
        record.add_birthday(bday)
        return "Birthday added."
    else:
        raise KeyError


@input_error
def show_birthday(book, name):
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value
    elif not record.birthday:
        return "Birthday not set for this contact."
    else:
        raise KeyError


def main():
    book = AddressBook()
    filename = 'address_book.pkl'
    if os.path.exists(filename):
        book.load_from_file(filename)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            book.save_to_file(filename)
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) != 2:
                print("Give me name and phone please.")
            else:
                name, phone = args
                print(add_contact(book, name, phone))
        elif command == "change":
            if len(args) != 2:
                print("Give me name and phone please.")
            else:
                name, phone = args
                print(change_contact(book, name, phone))
        elif command == "phone":
            if len(args) != 1:
                print("Enter user name.")
            else:
                name = args[0]
                print(show_phone(book, name))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            if len(args) != 2:
                print("Give me name and birthday please.")
            else:
                name, bday = args
                print(add_birthday(book, name, bday))
        elif command == "show-birthday":
            if len(args) != 1:
                print("Enter user name.")
            else:
                name = args[0]
                print(show_birthday(book, name))
        else:
            print("Command not recognized.")


if __name__ == "__main__":
    main()
