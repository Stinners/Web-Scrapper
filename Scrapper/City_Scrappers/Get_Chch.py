# Currently just returning an empty feild for extra infro for Chch
# getting this will require following the link to each individual
# consultation page and extracting the text from there

# Note in general returning an empty string means the receiving
# function will ignore the output

import datetime
import arrow
from utilities import get_html, add_elem
# - get_html retreives htm from an address and returns it as a soup
# - add_elem takes a list and an element and adds the element to the
#    list if non empty, this is used when searches could return blank feilds

domain =  "https://ccc.govt.nz"
chch_adress = domain + "/the-council/consultations-and-submissions/haveyoursay/"

def get_date(url):
    soup = get_html(url)
    arrow_date = arrow.get(soup.text, "- Do MMMM YYYY")
    return arrow_date.datetime

def christchurch():
    try:
        soup = get_html(chch_adress)
    except ValueError:         # Cannot retreive html
        print("Invalid Adress: Christchurch")
        return []
    consults = []
    subs_holders = soup.find_all("div", class_="tier2-contents")
    for sub in subs_holders:
        name = sub.find("div", class_="tier2-header").text.strip()
        details_url = domain + sub.find('a').get("href")
        extra_info = sub.find("div", class_="tier2-details").find("p").text.strip()
        date = get_date(details_url)
        consults.append([name, details_url, date, extra_info, []])
    return consults
