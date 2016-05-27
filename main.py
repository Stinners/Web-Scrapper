#! /usr/bin/env python3

# main file to handle the high level function calls

import get                               # header importing functions that retrive and parse the data for each region
from utilities import tag_submissions

# Each 'get' function returns a list of consultations, each consultation is iself
# represented as a list in the format:
#
#     [name, link, date, extra_info, tags]
#
# The first 4 feilds are strings and the last a list of strings
# Some may be returned empty depending on what is on the webpage
# Currently the tags list is returned empty and populated by a seperate function.

if __name__ == "__main__":

    chch_consults = get.christchurch()
    well_consults = get.wellington()

    chch_consults = tag_submissions(chch_consults, "Transport", ["parking", "cycling"])

    for consult in chch_consults:
        print(consult[0] + " Tags: " + str(consult[4]))
