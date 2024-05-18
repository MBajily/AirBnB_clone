#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.state import State


def parse(arg):
    curlyBraces = re.search(r"\{(.*?)\}", arg)
    brckts = re.search(r"\[(.*?)\]", arg)
    if curlyBraces is None:
        if brckts is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brckts.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brckts.group())
            return retl
    else:
        lexer = split(arg[:curlyBraces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curlyBraces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default for cmd module when input is invalid"""
        argsDict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argList = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argList[1])
            if match is not None:
                command = [argList[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argsDict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argsDict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argList = parse(arg)
        if len(argList) == 0:
            print("** class name missing **")
        elif argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argList[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argList = parse(arg)
        objDict = storage.all()
        if len(argList) == 0:
            print("** class name missing **")
        elif argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argList) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argList[0], argList[1]) not in objDict:
            print("** no instance found **")
        else:
            print(objDict["{}.{}".format(argList[0], argList[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argList = parse(arg)
        objDict = storage.all()
        if len(argList) == 0:
            print("** class name missing **")
        elif argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argList) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argList[0], argList[1]) not in objDict.keys():
            print("** no instance found **")
        else:
            del objDict["{}.{}".format(argList[0], argList[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argList = parse(arg)
        if len(argList) > 0 and argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argList) > 0 and argList[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argList) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argList = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argList[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argList = parse(arg)
        objDict = storage.all()

        if len(argList) == 0:
            print("** class name missing **")
            return False
        if argList[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argList) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argList[0], argList[1]) not in objDict.keys():
            print("** no instance found **")
            return False
        if len(argList) == 2:
            print("** attribute name missing **")
            return False
        if len(argList) == 3:
            try:
                type(eval(argList[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argList) == 4:
            obj = objDict["{}.{}".format(argList[0], argList[1])]
            if argList[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argList[2]])
                obj.__dict__[argList[2]] = valtype(argList[3])
            else:
                obj.__dict__[argList[2]] = argList[3]
        elif type(eval(argList[2])) == dict:
            obj = objDict["{}.{}".format(argList[0], argList[1])]
            for k, v in eval(argList[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
