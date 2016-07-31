#! /usr/bin/env python3

# This script can be used to add data to the Django databases

import os
import sys
import django

# ---------------------------------------------------------
#     Setting up the environemnt to access the database
# ---------------------------------------------------------

# Setting up system variables
# location of django modules
website_path = "/home/chris/Code/Python/Web-Scrapper/django_site"
sys.path.append(website_path)
os.environ['DJANGO_SETTINGS_MODULE'] = "django_site.settings"

# Setting up the Django db API
# This allows the script to interact with the models in
# exactly the same way as 'manage.py shell'
django.setup()

# Read data from an input file
# The data is in a list of tuples (city-name, [subs-list])
# Each sub list has the format [name, link, date, extra_info, tags]

# ---------------------------------------------------------
#                       Functions
# ---------------------------------------------------------

import pickle
from django.utils.timezone import make_aware
from get_data.models import Submission, Tag

def update_data(data):
    # Clear all the old data from the database
    Submission.objects.all().delete()
    Tag.objects.all().delete()
    # Add all the new data
    for city in data:
        city_name = city[0]
        subs = city[1]
        for sub in subs:
            add_sub(sub, city_name)


def add_sub(sub, city_name):
    # Create and save an entry in Submissions
    entry = Submission(name       = sub[0],
                       city       = city_name,
                       link       = sub[1],
                       extra_info = sub[3],
                       date       = make_aware(sub[2])) # make_aware stops django from complaining about lack of timezone
    entry.save()

    for tag in sub[4]:
        tag_entry, created = Tag.objects.get_or_create(tag_name = tag)
        if created:
            tag_entry.save()
        entry.tags.add(tag_entry)

# ---------------------------------------------------------
#  Main block for actually adding the data to the database
# ---------------------------------------------------------

if __name__ == "__main__":
    #  Read data from an input file
    #  The data is in a list of tuples (city-name, [subs-list])
    #  Each sub list has the format [name, link, date, extra_info, tags]
    if len(sys.argv) == 1:
        print("Please give the input file")
        sys.exit()
    infile_name = sys.argv[1]
    try:
        input_file = open(infile_name, 'rb')
    except:
        print("Could not open file " + infile_name)
        sys.exit()
    data = pickle.load(input_file)
    input_file.close()

    # Store the data in the database
    update_data(data)
