#! /usr/bin/env python3

# main file to handle the high level function calls

# Each 'get' function returns a list of consultations, each consultation is itself
# represented as a list in the format:
# Possibly rewrite this as a dict to avoid the ordering problem
#
#     [name, link, date, extra_info, tags]
#
# name, link and extra_info are strings and tags is as empty list
# Other feilds may be returned empty depending on what's on the webpage
# Currently the tags list is returned empty and populated by a seperate function.

# The date is a raw python datetime object

# The final output of main is a dict where the keys are the city names and the values
# are lists of submissions in the format described above

import datetime
import pickle
from utilities import tag_submissions, check_size
import City_Scrappers as get                        # header importing functions that retrive and parse the data for each region


def process_cities(*get_functions):
    """ Calls each 'get.city' function in turn and then applies tagging functions
        returns the list containing all the output  """
    results = {}
    for get_city in get_functions:
        city = get_city.__name__     # reading the city name from the function itself - there must be a better way to do this
        subs = get_city()
        subs = tag_submissions(subs, "transport", ["parking", "cycling"])   # Move this into a seperate data structure
        results[city] = subs
    return results

if __name__ == "__main__":

    consults = process_cities(get.christchurch,
                              get.wellington)

    # Find a better way to send this to the db
    # The simplest way would just be JSON with a key for security
    # Probably just run the search on the server
    with open("../output.txt", "wb") as File:
        pickle.dump(consults, File)
