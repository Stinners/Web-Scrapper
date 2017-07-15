
# Run this using unittest's dicovery mechanism
# python3 -m unittest
# from Flask_Site

# Add some tests to ensure the tags are managed properly

# Problem currentluy is that the database targeted is determined bu the models in db.py which
# all inherit from a meta class that just laods the data from that file

import unittest
from datetime import datetime

from peewee import MySQLDatabase
from playhouse.test_utils import test_database

import db
from db import Submission, Tag, Submission_Tag
import local_config as local

strptime = datetime.strptime

# Assuming the testing db is accessed by the same user as the
# production db
test_db = MySQLDatabase(local.test_db_name,
                   host=local.host,
                   user=local.user,
                   passwd=local.passwd)

# Test data
# Layed out like this to make it easy to construct the expected results
lion_sub_tags = ["Lion Regulations", "", strptime("3000","%Y"), "", ["wildlife"]]
ollifant_sub_tags = ["Ollifant Rights", "", strptime("3000", "%Y"), "", ["wildlife"]]
rail_sub_tags = ["Safty Rail Standards", "", strptime("1970", "%Y"), "",  []]
test_data = {"narnia": [lion_sub_tags],
             "gondor": [ollifant_sub_tags, rail_sub_tags]}

# Removing the tags part of the list since it isn;t returned
# in from the database
lion_sub = lion_sub_tags[0:4]
ollifant_sub = ollifant_sub_tags[0:4]
rail_sub = rail_sub_tags[0:4]

def db_test(func):
    """ Decorator which takes a function and wraps it in a
        test_db context manager """
    def with_test_db(*args, **kwargs):
        with test_database(test_db, (Submission, Tag, Submission_Tag), create_tables=False):
            return func(*args, **kwargs)
    return with_test_db


class TestDB(unittest.TestCase):

    @classmethod
    @db_test
    def setUpClass(self):
        db.reset_db(test_db)
        db.add_subs(test_data)

    @classmethod
    @db_test
    def tearDownClass(self):
        db.delete_tables(test_db)

    def make_test(city, tag, results_list):
        @db_test
        def new_test(self):
            self.assertCountEqual(db.get_subs(city, tag), results_list)
        return new_test

    test_lookup_all = make_test("all", "all", [lion_sub, ollifant_sub, rail_sub])
    test_look_tags = make_test("all", "wildlife", [lion_sub, ollifant_sub])
    test_look_city = make_test("gondor", "all", [ollifant_sub, rail_sub])
    test_city_and_tag = make_test("gondor", "wildlife", [ollifant_sub])
    test_find_nothing = make_test("utopia", "chamber pots", [])

# A module for test which require modifying the database contents
class TestDBModify(unittest.TestCase):

    @db_test
    def setUp(self):
        db.reset_db(test_db)
        db.add_subs(test_data)

    @db_test
    def tearDown(self):
        db.delete_tables(test_db)

    @db_test
    def test_clean(self):
        db.clean_db()
        self.assertCountEqual(db.get_subs("any", "any"), [lion_sub, ollifant_sub])
