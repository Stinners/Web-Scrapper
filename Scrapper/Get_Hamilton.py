# Hamilton does not have submission details on a single page and does not
# give information in any consistent format. Thus this script will need to go
# to the main 'haev your say' page, then follow the links to each of the
# individual submission pages and extract the data from them using heuristics

from utilities import get_html

domain_name = "http://www.hamilton.govt.nz/"
hamilton_adress = "http://www.hamilton.govt.nz/our-council/consultation-and-public-notices/haveyoursay/Pages/default.aspx"

def hamilton():
    try:
        soup = get_html(hamilton_adress)
    except:
        return("Invalid Adress: Christchurch")

    subs = []
    # Need to find the links to the individual submission pages
    # These are contained in the first of two  unordered lists
    # with the class "dccw-authoringElement-Body"
    open_subs = soup.findAll('ul' ,{"class" : "dccw-authoringElement-Body"})[0]
    for sub in open_subs.findAll('a'):
        name = sub.text
        link = domain_name + sub['href']
        # Extract the date (as a string) from from the inner page
        date = get_date(link)
    return None

def get_date(link):
    try:
        soup = get_html(link)
    except:
        return("Could not find submission page - Hamilton")

    # This function will need to indentify the text string corresponding to the
    # closing date from human frendly text and then be able to parse that date
    # Without a specified format

    # Extract the text
    # Split it into sentences
    # Look for key phrases indicating closure
    # Find the date in that sentence
    # Parse the date
    # preform sanity checks (or maybe even ask the user for confimation)
