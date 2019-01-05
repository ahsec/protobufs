#!/usr/bin/env python
""" My own, very first practical use of a protocol buffer.
"""
import argparse
from addressbook_pb2 import person_pb2

def argument_parser():
    """Argument parser function.
    Reads the Addressbook name from the commandline.
    Returns an Argument parser object.
    """
    parsed = argparse.ArgumentParser(description="""Creates or appends data to
                                an addressbook file""")
    parsed.add_argument("f", help="Filename of existing or new Addressbook")
    return parsed

def read_addrbook(addrbook, fname):
    """Read existing address book file or creates a new one if fname does not
    exist.
    """
    try:
        with open(fname, "rb") as fopen:
            addrbook.ParseFromString(fopen.read())
    except IOError:
        print("[!] Address book file \"{}\" doesn't exist.".format(fname))
        print("    Creating new file")

def write_addrbook(addrbook, fname):
    """Write collected addrbook data in fname file.
    """
    try:
        with open(fname, "wb") as fopen:
            fopen.write(addrbook.SerializeToString())
    except IOError:
        SystemExit("[X] Error: Can not write file {}".format(fname))

def print_addbook(addrbook):
    """Prints the content of an addressbook
    """
    for people in addrbook.people:
        print("Name: {}".format(people.name))
        print("  ID: {}".format(people.id))
        if people.email:
            print("  email: {}".format(people.email))
        for phone in people.phones:
            print("  Phone number: {}".format(phone.number))
            if phone.type:
                print("    Phone type: {}".format(phone.type))
        print("\n")
    else:
        print("End of Address book content")

def prompt_entry(person):
    """Prompts for Person information to be added to the new Addressbook.
    """
    person.id = int(raw_input("Person ID: "))
    person.name = raw_input("Person name: ")
    email = raw_input("Person email, leave blank for none: ")
    person.email = email if email else ""
    while True:
        number = raw_input("Person phone number(s), leave blank to finish: ")
        if not number:
            break
        phonenumber = person.phones.add()
        phonenumber.number = number
        num_type = raw_input("Type of number (mobile / home / work): ")
        if num_type in ["mobile", "Mobile", "MOBILE"]:
            phonenumber.type = person.MOBILE
        elif num_type in ["home", "Home", "HOME"]:
            phonenumber.type = person.HOME
        elif num_type in ["work", "Work", "WORK"]:
            phonenumber.type = person.WORK
        else:
            print("Unkown phone number type. Leaving as default")

def main():
    """Prompts user for new entries to add to the addressbook.
    """
    parsed = argument_parser()
    args = parsed.parse_args()
    fname = args.f

    addrbook = person_pb2.AddressBook()
    read_addrbook(addrbook, fname)

    welcome_msg = """\n\nDo you want to
            (p)rint existing entries
            (a)dd a new entry
            (e)xit"""

    while True:
        print(welcome_msg)
        option = raw_input("Option: ")
        if option in ["p","P"]:
            print_addbook(addrbook)
        elif option in ["a","A"]:
            prompt_entry(addrbook.people.add())
            write_addrbook(addrbook, fname)
            print("\n[*] New Addressbook entry successfully written")
        elif option in ["e","E"]:
            print("Exiting")
            break
        else:
          print(welcome_msg)
          option = raw_input("Option: ")

if __name__ == "__main__":
    main()
