from collections import UserDict
from datetime import datetime
import re
import pickle
import pathlib
from os import chdir, getcwd

FILE_NAME = 'my_records.bin'
def input_error(func):
    def inner(base_command, command, contacts):
        try:
            return func(base_command, command, contacts)
        except KeyError:
            return 'The command is not exist'
            
        except PhoneValueError:
            return 'Phone number must consist of numbers'
        
        except IndexError:
            return 'Not given name or phone number'
        
        except NameError:
            return ' Not given name'

        except BirthdayDateError:
            return "Birthday date is incorrect or contact's birthday date already exists"
    return inner

class PhoneValueError(Exception):
    pass 

class BirthdayDateError(Exception):
    pass

class NameError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value
    
class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.phone
    
    @value.setter
    def value(self, value):
        if not value.isdigit():
            raise PhoneValueError
        else:
            self.phone = value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__birthday
    
    @value.setter
    def value(self, value):
        birthday = re.split(r'[\D]+', value)
        if len(birthday) < 3:
            raise BirthdayDateError
        else:
            if len(birthday[0]) <= 2:
                birthday.reverse()
            try:
                self.__birthday = datetime(year= int(birthday[0]), month= int(birthday[1]), day=int(birthday[2])).date()
            except:
                raise BirthdayDateError


class Record:
    def __init__(self, contact_name):
        self.name = Name(contact_name).value
        self.phone_num = []
        self.birthday = None

    def add_phone(self, phone):
        self.phone_num.append(Phone(phone).value)

    def remove_phone(self, phone):
        self.phone_num.remove(Phone(phone).value)

    def change_phone(self, phone, new_phone):
        self.phone_num.remove(Phone(phone).value)
        self.phone_num.append(Phone(new_phone).value)

    def set_birthday(self, birthday):
        if self.birthday == None:
            self.birthday = Birthday(birthday).value
        else:
            raise BirthdayDateError
        
    def days_to_birthday(self):
        if self.birthday != None:
            todays_date = datetime.today().date()
            abs_birthday_date = self.birthday.replace(year=todays_date.year)

            if abs_birthday_date < todays_date:
                abs_birthday_date = self.birthday.replace(year=todays_date.year + 1)

            days_to_birthday  = abs(todays_date - abs_birthday_date).days
            return days_to_birthday
        else:
            return f'Unknown contact\'s birthday date'
            

class AdressBook(UserDict):
    def add_record(self, name):
        self.data[Record(name).name] = Record(name)

    def show_all(self):
        all_contacts = ''
        for contact, phones in self.data.items():
            all_contacts += f'Name: {str(contact):<10} Phone number: {phones.phone_num} Birthday: {phones.birthday}\n'
        return all_contacts
    
    def find_contact(self, searched_slice):
        found_contacts = ''
        for contact, phones in self.data.items():
            if searched_slice in str(contact) or searched_slice in str(phones.phone_num):
                found_contacts += f'Name: {str(contact):<10} Phone number: {phones.phone_num} Birthday: {phones.birthday}\n'
        return found_contacts
       
    def iterator(self):
        N = 2
        for contact, phones in self.data.items():
            i = 0
            while i < N:
                cont = f'Name: {str(contact):<10} Phone number: {phones.phone_num} Birthday: {phones.birthday}'
                i += 1
            yield cont
        

def hello(command, contacts):
    return 'How can I help you?'

def create_contact(command, contacts):
    try:
        name = command[1]
    except:
        raise NameError
    
    if list(contacts.keys()) == []:
        return contacts.add_record(name)

    for contact in contacts.keys():
        if name == str(contact):
            return 'The contact already exists'
        
    return contacts.add_record(name)

def add_phone(command, contacts):
    try:
        name = command[1]
    except:
        raise NameError
    
    try:
        phone =command[2]
    except:
        raise PhoneValueError
    for contact, phones in contacts.items():
        if name == str(contact) and phone not in phones.phone_num:
            phones.add_phone(phone)
            return
    return "The contact doesn't exists or phone number was already added"

def change_phone_num(command, contacts):
    try:
        name = command[1]
    except:
        raise NameError
    try:
        phone_num, new_phone = command[2], command[3]
    except:
        raise PhoneValueError
    
    for contact, phones in contacts.items():
        if name == str(contact) and phone_num in phones.phone_num:
            phones.change_phone(phone_num, new_phone)
            return
    return "The contact or phone number doesn't exists"

def show_contact(command, contacts):
    try:
        name = command[1]
    except:
        raise NameError
    for contact, phones in contacts.items():
        if name == str(contact):
            return f'contact name: {str(contact)}; phones: {phones.phone_num}'
    
    return f"contact name: {name} doesn't exists"

def delete_phone(command, contacts):
    try:
        name = command[1]
    except:
        raise NameError
    try:
        phone =command[2]
    except:
        raise PhoneValueError
    for contact, phones in contacts.items():
        if name == str(contact) and phone in (phones.phone_num):
            phones.remove_phone(phone)
            return
        
    return "The contact or phone number doesn't exists"
    
def show_all(command, contacts):
    return contacts.show_all()

def end_program(command, contacts):
    return False

def accepted_commands(command, contacts):
    commands = (list(OPERATIONS.keys()))
    message = ''
    for command in commands:
        message += f'"{command}" '
        
    return f"Accepted commands: {message}"

def set_birthday(command, contacts):
    try:
        name = command[1]
    except:
        raise NameError
    try:
        birthday =  command[2]
    except:
        raise BirthdayDateError
    for contact, contact_data in contacts.items():
        if name == str(contact):
            contact_data.set_birthday(birthday)
            return
    return "The contact doesn't exists"
    
def days_to_birthday(command, contacts):
    try:
        name = command[1]
    except:
        raise NameError
    for contact, birthday in contacts.items():
        if name == str(contact):
            return f'contact name: {str(contact)}; days to birthday: {birthday.days_to_birthday()}'
    
    return f"contact name: {name} doesn't exists"

def iterator(command, contacts):
    '''Blank function. Real Iterator is localized in "main" function'''
    pass

def find_contact(command, contacts):
    searched_slice = command[1]
    return contacts.find_contact(searched_slice)

def read_from_file(file_name):
    with open(file_name, 'rb') as fh:
        contacts = pickle.load(fh)
        return contacts
    
def write_to_file(file_name, contacts):
    with open(file_name, 'wb') as fh:
        pickle.dump(contacts, fh)
        return contacts
    

OPERATIONS = {
    'accepted_commands':accepted_commands,
    'hello': hello,
    'create_contact': create_contact,
    'add_phone': add_phone,
    'change_phone_num': change_phone_num,
    'show_contact': show_contact,
    'delete_phone': delete_phone,
    'set_birthday' : set_birthday,
    'days_to_birthday': days_to_birthday,
    'iterator': iterator,
    'show_all': show_all,
    'find_contact' : find_contact,
    'good_bye': end_program, 
    'close': end_program, 
    'exit': end_program, 
    '.': end_program, 
}

@input_error
def handler_command(base_command, command, contacts):
    return OPERATIONS[base_command](command, contacts)

def main():
    flag = True
    if pathlib.Path(FILE_NAME).is_file():
        contacts = read_from_file(FILE_NAME)
    else:
        contacts = AdressBook()
    print(accepted_commands(OPERATIONS, contacts))
    while flag:
        command = input('Write your command: ').lower().strip().split()

        try:
            base_command = command[0]
        except IndexError:
            continue
        
        handler = handler_command(base_command, command, contacts)

        if isinstance(handler, str) or base_command == 'iterator':
            if base_command == 'iterator':
                for c in contacts:
                    print(c)
            else:
                print(handler)
        
        elif isinstance(handler, bool):
            write_to_file(FILE_NAME, contacts)
            flag = handler

        else:
            handler


if __name__ == '__main__':
    main()
