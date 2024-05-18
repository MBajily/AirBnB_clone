#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestCityInstantiation
    TestCitySave
    TestCityToDict
"""
import os
import models
import unittest
from datetime import datetime
# from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_two_models_unique_ids(self):
        cm1 = City()
        cm2 = City()
        self.assertNotEqual(cm1.id, cm2.id)

    def test_two_models_different_created_at(self):
        cm1 = City()
        # sleep(0.05)
        cm2 = City()
        self.assertLess(cm1.created_at, cm2.created_at)

    def test_two_models_different_updated_at(self):
        cm1 = City()
        # sleep(0.05)
        cm2 = City()
        self.assertLess(cm1.updated_at, cm2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        cm = City()
        cm.id = "123456"
        cm.created_at = cm.updated_at = dt
        cmstr = cm.__str__()
        self.assertIn("[City] (123456)", cmstr)
        self.assertIn("'id': '123456'", cmstr)
        self.assertIn("'created_at': " + dt_repr, cmstr)
        self.assertIn("'updated_at': " + dt_repr, cmstr)

    def test_args_unused(self):
        cm = City(None)
        self.assertNotIn(None, cm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cm = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cm.id, "345")
        self.assertEqual(cm.created_at, dt)
        self.assertEqual(cm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cm = City("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cm.id, "345")
        self.assertEqual(cm.created_at, dt)
        self.assertEqual(cm.updated_at, dt)


class TestCitySave(unittest.TestCase):
    def test_one_save(self):
        cm = City()
        first_updated_at = cm.updated_at
        cm.save()
        self.assertLess(first_updated_at, cm.updated_at)

    def test_two_saves(self):
        cm = City()
        first_updated_at = cm.updated_at
        cm.save()
        second_updated_at = cm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        cm.save()
        self.assertLess(second_updated_at, cm.updated_at)

    def test_save_with_arg(self):
        cm = City()
        with self.assertRaises(TypeError):
            cm.save(None)

    def test_save_updates_file(self):
        cm = City()
        cm.save()
        cmid = "City." + cm.id
        with open("file.json", "r") as f:
            self.assertIn(cmid, f.read())


class TestCityToDict(unittest.TestCase):
    def test_to_dict_type(self):
        cm = City()
        self.assertTrue(dict, type(cm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        cm = City()
        self.assertIn("id", cm.to_dict())
        self.assertIn("created_at", cm.to_dict())
        self.assertIn("updated_at", cm.to_dict())
        self.assertIn("__class__", cm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        cm = City()
        cm.name = "John Doe"
        cm.age = 25
        cm_dict = cm.to_dict()
        self.assertIn("name", cm_dict)
        self.assertIn("age", cm_dict)
        self.assertEqual(cm_dict["name"], "John Doe")
        self.assertEqual(cm_dict["age"], 25)


if __name__ == "__main__":
    unittest.main()
