#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommandprompting
    TestHBNBCommandhelp
    TestHBNBCommandexit
    TestHBNBCommandcreate
    TestHBNBCommandshow
    TestHBNBCommandall
    TestHBNBCommanddestroy
    TestHBNBCommandupdate
"""
import os
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommandprompting(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", otpt.getvalue().strip())


class TestHBNBCommandhelp(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(self):
        help = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help_create(self):
        help = ("Usage: create <class>\n        "
            "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help_EOF(self):
        help = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help_show(self):
        help = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help_destroy(self):
        help = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help_all(self):
        help = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objects.")
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help_count(self):
        help = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help_update(self):
        help = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(help, otpt.getvalue().strip())

    def test_help(self):
        help = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(help, otpt.getvalue().strip())


class TestHBNBCommandexit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandcreate(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        crct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_create_invalid_class(self):
        crct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_create_invalid_syntax(self):
        crct = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        crct = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(otpt.getvalue().strip()))
            testKey = "BaseModel.{}".format(otpt.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(otpt.getvalue().strip()))
            testKey = "User.{}".format(otpt.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(otpt.getvalue().strip()))
            testKey = "State.{}".format(otpt.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(otpt.getvalue().strip()))
            testKey = "City.{}".format(otpt.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(otpt.getvalue().strip()))
            testKey = "Amenity.{}".format(otpt.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(otpt.getvalue().strip()))
            testKey = "Place.{}".format(otpt.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(otpt.getvalue().strip()))
            testKey = "Review.{}".format(otpt.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


class TestHBNBCommandshow(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class(self):
        crct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_show_invalid_class(self):
        crct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        crct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        crct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        crct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        crct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "show BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["User.{}".format(testID)]
            command = "User.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["State.{}".format(testID)]
            command = "State.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Place.{}".format(testID)]
            command = "Place.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["City.{}".format(testID)]
            command = "City.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "Amenity.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Review.{}".format(testID)]
            command = "Review.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), otpt.getvalue().strip())


class TestHBNBCommanddestroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def test_destroy_missing_class(self):
        crct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_destroy_invalid_class(self):
        crct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        crct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        crct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        crct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        crct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "destroy BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["User.{}".format(testID)]
            command = "User.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["State.{}".format(testID)]
            command = "State.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Place.{}".format(testID)]
            command = "Place.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["City.{}".format(testID)]
            command = "City.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "Amenity.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            obj = storage.all()["Review.{}".format(testID)]
            command = "Review.destory({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())


class TestHBNBCommandall(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_invalid_class(self):
        crct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_all_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", otpt.getvalue().strip())
            self.assertIn("User", otpt.getvalue().strip())
            self.assertIn("State", otpt.getvalue().strip())
            self.assertIn("Place", otpt.getvalue().strip())
            self.assertIn("City", otpt.getvalue().strip())
            self.assertIn("Amenity", otpt.getvalue().strip())
            self.assertIn("Review", otpt.getvalue().strip())

    def test_all_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", otpt.getvalue().strip())
            self.assertIn("User", otpt.getvalue().strip())
            self.assertIn("State", otpt.getvalue().strip())
            self.assertIn("Place", otpt.getvalue().strip())
            self.assertIn("City", otpt.getvalue().strip())
            self.assertIn("Amenity", otpt.getvalue().strip())
            self.assertIn("Review", otpt.getvalue().strip())

    def test_all_single_object_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", otpt.getvalue().strip())
            self.assertNotIn("User", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())

    def test_all_single_object_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", otpt.getvalue().strip())
            self.assertNotIn("User", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", otpt.getvalue().strip())
            self.assertNotIn("BaseModel", otpt.getvalue().strip())


class TestHBNBCommandupdate(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_missing_class(self):
        crct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_invalid_class(self):
        crct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        crct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_missing_id_dot_notation(self):
        crct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        crct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_invalid_id_dot_notation(self):
        crct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        crct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = otpt.getvalue().strip()
            testCmd = "update BaseModel {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = otpt.getvalue().strip()
            testCmd = "update User {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = otpt.getvalue().strip()
            testCmd = "update State {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = otpt.getvalue().strip()
            testCmd = "update City {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = otpt.getvalue().strip()
            testCmd = "update Amenity {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = otpt.getvalue().strip()
            testCmd = "update Place {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(self):
        crct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = otpt.getvalue().strip()
            testCmd = "BaseModel.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = otpt.getvalue().strip()
            testCmd = "User.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = otpt.getvalue().strip()
            testCmd = "State.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = otpt.getvalue().strip()
            testCmd = "City.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = otpt.getvalue().strip()
            testCmd = "Amenity.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = otpt.getvalue().strip()
            testCmd = "Place.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        crct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create BaseModel")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "update BaseModel {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create User")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "update User {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create State")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "update State {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create City")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "update City {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Amenity")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "update Amenity {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "update Place {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Review")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "update Review {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(self):
        crct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create BaseModel")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "BaseModel.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create User")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "User.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create State")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "State.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create City")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "City.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Amenity")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "Amenity.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "Place.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Review")
            testId = otpt.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as otpt:
            testCmd = "Review.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(crct, otpt.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create BaseModel")
            testId = otpt.getvalue().strip()
        testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create User")
            testId = otpt.getvalue().strip()
        testCmd = "update User {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create State")
            testId = otpt.getvalue().strip()
        testCmd = "update State {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create City")
            testId = otpt.getvalue().strip()
        testCmd = "update City {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "update Place {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Amenity")
            testId = otpt.getvalue().strip()
        testCmd = "update Amenity {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Review")
            testId = otpt.getvalue().strip()
        testCmd = "update Review {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def test_update_valid_string_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create BaseModel")
            tId = otpt.getvalue().strip()
        testCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create User")
            tId = otpt.getvalue().strip()
        testCmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create State")
            tId = otpt.getvalue().strip()
        testCmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create City")
            tId = otpt.getvalue().strip()
        testCmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            tId = otpt.getvalue().strip()
        testCmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Amenity")
            tId = otpt.getvalue().strip()
        testCmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Review")
            tId = otpt.getvalue().strip()
        testCmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_int_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "update Place {} max_guest 98".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_int_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            tId = otpt.getvalue().strip()
        testCmd = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "update Place {} latitude 7.2".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_float_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            tId = otpt.getvalue().strip()
        testCmd = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_dictionary_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create BaseModel")
            testId = otpt.getvalue().strip()
        testCmd = "update BaseModel {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create User")
            testId = otpt.getvalue().strip()
        testCmd = "update User {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create State")
            testId = otpt.getvalue().strip()
        testCmd = "update State {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create City")
            testId = otpt.getvalue().strip()
        testCmd = "update City {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Amenity")
            testId = otpt.getvalue().strip()
        testCmd = "update Amenity {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Review")
            testId = otpt.getvalue().strip()
        testCmd = "update Review {} ".format(testId)
        testCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create BaseModel")
            testId = otpt.getvalue().strip()
        testCmd = "BaseModel.update({}".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create User")
            testId = otpt.getvalue().strip()
        testCmd = "User.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create State")
            testId = otpt.getvalue().strip()
        testCmd = "State.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create City")
            testId = otpt.getvalue().strip()
        testCmd = "City.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Amenity")
            testId = otpt.getvalue().strip()
        testCmd = "Amenity.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Review")
            testId = otpt.getvalue().strip()
        testCmd = "Review.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "update Place {} ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            HBNBCommand().onecmd("create Place")
            testId = otpt.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])


class TestHBNBCommandcount(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", otpt.getvalue().strip())

    def test_count_object(self):
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", otpt.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as otpt:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", otpt.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
