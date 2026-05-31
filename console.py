#!/usr/bin/python3
"""This module defines the entry point of the AirBnB clone command interpreter.

The console provides an interactive shell to manage AirBnB objects
using either FileStorage or DBStorage depending on HBNB_TYPE_STORAGE.
"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def parse(line):
    """Parse a command line string into a list of arguments.

    Handles quoted strings and removes extra whitespace.

    Args:
        line (str): The raw command line string.

    Returns:
        list: A list of argument strings.
    """
    curly_braces = re.search(r"\{(.*?)\}", line)
    brackets = re.search(r"\[(.*?)\]", line)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in line.split()]
        else:
            lexer = line[:brackets.span()[0]].split()
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = line[:curly_braces.span()[0]].split()
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """HBNBCommand implements the AirBnB clone command interpreter.

    Supports object creation with parameters:
        create <Class> <key>=<value> ...

    Attributes:
        prompt (str): The command prompt displayed to the user.
        __classes (list): List of valid model class names.
    """

    prompt = "(hbnb) "
    __classes = [
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    ]

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def default(self, line):
        """Handle commands in the form <class>.<command>(<args>).

        Args:
            line (str): The input command line.
        """
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            argl = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Create a new instance with given parameters, save it, and print id.

        Usage: create <class> [<key>=<value> ...]

        Value formats:
            String: "<value>" (double-quoted, underscores become spaces)
            Float:  <unit>.<decimal>
            Integer: <number>

        Invalid parameters are silently skipped.
        """
        argl = line.split()
        if len(argl) == 0:
            print("** class name missing **")
            return
        class_name = argl[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        new_obj = eval(class_name)()

        for param in argl[1:]:
            match = re.match(r'^(\w+)=(.+)$', param)
            if not match:
                continue
            key = match.group(1)
            value_str = match.group(2)

            # String value: starts and ends with double-quote
            if re.match(r'^".*"$', value_str):
                value = value_str[1:-1]
                # Replace escaped quotes and underscores
                value = value.replace('\\"', '"').replace('_', ' ')
                setattr(new_obj, key, value)
            else:
                # Try float (must contain a dot)
                try:
                    if '.' in value_str:
                        value = float(value_str)
                        setattr(new_obj, key, value)
                    else:
                        value = int(value_str)
                        setattr(new_obj, key, value)
                except ValueError:
                    continue

        new_obj.save()
        print(new_obj.id)

    def do_show(self, line):
        """Print the string representation of an instance.

        Usage: show <class> <id>
        """
        argl = parse(line)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, line):
        """Delete an instance based on class name and id.

        Usage: destroy <class> <id>
        """
        argl = parse(line)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, line):
        """Print string representations of all instances, optionally by class.

        Usage: all [class]
        """
        argl = parse(line)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and obj.__class__.__name__ == argl[0]:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, line):
        """Count the number of instances of a given class.

        Usage: count <class>
        """
        argl = parse(line)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, line):
        """Update an instance by adding or updating an attribute.

        Usage: update <class> <id> <attribute name> <attribute value>
        """
        argl = parse(line)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except (NameError, SyntaxError):
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
