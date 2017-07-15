#! /usr/bin/env python3

# This file contains functions for interacting with the database

# start and stop the server using
# /etc/init.d/mysql start
# /etc/init.d/mysql stop

# Need to impliment connection polling

import datetime
import json
import pickle
from peewee import (CharField, TextField, DateTimeField, ForeignKeyField,
                    MySQLDatabase, Model)


import local_config as local

db = MySQLDatabase(local.db_name,
                   host=local.host,
                   user=local.user,
                   passwd=local.passwd)

class BaseModel(Model):
    """ The internal class Meta specifies that this model corresponds
    to a table in the database 'db', we can then allow all other tables
    in db to inherit from this class """
    class Meta:
        database = db

# Models

# Possible reimpliment cities as a forign key

class Submission(BaseModel):
    name       = TextField()
    city       = TextField()
    link       = TextField()
    date       = DateTimeField()
    extra_info = TextField()

class Tag(BaseModel):
    tag = CharField(max_length=50)

# This tables stores the relationships bewteen
# the submissions and tags
class Submission_Tag(BaseModel):
    sub = ForeignKeyField(Submission)
    tag = ForeignKeyField(Tag)

###### Functions for interacting with Database

# Move migrations into a seperate file
def create_tables(this_db):
    this_db.create_tables([Submission, Tag, Submission_Tag])

def delete_tables(this_db):
    this_db.drop_tables([Submission, Tag, Submission_Tag])

def reset_db(this_db):
    try:
        delete_tables(this_db)
    except:
        pass
    try:
        create_tables(this_db)
    except:
        pass

def insert_sub(sub, city):
    """ Adds an entry for a submission to the database along with the
        correct connections for tagging """
    #sub has format [name, link, date, extra_info, tags]

    # check if the sub is already in the db, return if it does
    query = Submission.select().where(Submission.name == sub[1])
    if query.exists():
        return 0

    # if it doesn't exists add the entry
    new_sub = Submission.create(name = sub[0],
                                link = sub[1],
                                date = sub[2],
                                extra_info = sub[3],
                                city = city)

    # Check for any new tags in the sub and add if nessecary
    # Then update the many-to-many relationship table
    for sub_tag in sub[4]:
        tag_query = Tag.select().where(Tag.tag == sub_tag)
        if not tag_query.exists():
            Tag.create(tag = sub_tag)

        Submission_Tag.create(sub=new_sub, tag=tag_query.get())

def clean_db():
    """ Removes all the submissions that have closed and the coressponding
    Submission_Tag Rows """
    now = datetime.datetime.now()
    for sub in Submission.select():
        if now > sub.date:
            Submission_Tag.delete().where(sub == sub)
            sub.delete_instance()

def add_subs(subs_dic):
    """ Takes the dict of submissions produced by process_cities and
        saves the output to the database"""
    for (city, subs) in subs_dic.items():
        for sub in subs:
            insert_sub(sub, city)

# Probably don't use this in production
def get_subs_from_pickle(filepath):
    """ Read in subs from a pickle file """
    try:
        with open(filepath, "rb") as infile:
            subs = pickle.load(infile)
    except FileNotFoundError:               # Think about how to handel this error
        print("Could not read pickle file")
        import sys; sys.exit()
    return subs

def get_city(query, city_name):
    """ This function takes a city and a query and returns the query with a
        filter by city name applied """
    return query.where(Submission.city == city_name)

def get_tag(query, tag):
    return (query.join(Submission_Tag)
                 .join(Tag)
                 .where(Tag.tag == tag))

 #sub has format [name, link, date, extra_info, tags]
def unpack_sub(sub):
    # May be best to convert datetime to string here
    return [sub.name, sub.link, sub.date, sub.extra_info]

def get_subs(city, tag):
    """ Main interface for retreiving submissions from the db
        Takes a city name and tag and returns the subs that satify that criteria.
        Either of these arguments can be repaced with 'any' to return all
        tags or cities. """
    query = Submission.select()
    if city.lower() not in ["any", "all"]:
        query = get_city(query, city)
    if tag.lower() not in ["any", "all"]:
        query = get_tag(query, tag)
    return [unpack_sub(sub) for sub in query]

def get_json(city, tag):
    subs = get_subs(city, tag)
    for sub in subs:
        sub[2] = sub[2].strftime("%x %I:%M%p")
    return json.dumps(subs)

def get_cities_and_tags():
    """ Returns a list of all unique cities and tags in the database """
    cities = set([sub.city for sub in Submission.select()])
    tags = set([tag.tag for tag in Tag])   # Tags are unique but returning as a set for consitency with cities
    return cities, tags
