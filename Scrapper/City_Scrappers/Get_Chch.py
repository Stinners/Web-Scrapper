# Currently just returning an empty feild for extra infro for Chch
# getting this will require following the link to each individual
# consultation page and extracting the text from there

# Note in general returning an empty string means the receiving
# function will ignore the output

import datetime
from utilities import get_html, add_elem
# - get_html retreives htm from an address and returns it as a soup
# - add_elem takes a list and an element and adds the element to the
#    list if non empty, this is used when searches could return blank feilds

chch_adress = "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo/"

# Main Block

def christchurch():
    try:
        soup = get_html(chch_adress)
    except ValueError:         # Cannot retreive html
        print("Invalid Adress: Christchurch")
        return []
    try:
        table = soup.find("table").find_all("td")
    except AttributeError:    # No currently open consultations
        return []
    names = []; links = []; info = []; dates = []

    for row in table:
        names = add_elem(names, get_name(row))
        links = add_elem(links, get_link(row))
        dates = add_elem(dates, get_date(row))
    consults = [[names[i], links[i], dates[i], "", []] for i in range(len(names))]
    return(consults)

def get_name(row):
    try:
        name = row.find("a").get_text()
    except AttributeError:
        name = ''
    return name

def get_link(row):
    try:
        link = row.find("a").get("href")
        # ignoring the 'have your say' buttons and linking to the
        # consultation page, this requires the url be completed
        if "https" in link:
            link = ''
        else:
            link = chch_adress + link
    except AttributeError:
        link = ''
    return(link)

def get_date(row):
    text = row.text.strip()
    is_date = ("p.m" in text) or ("a.m" in text)
    if is_date:
        date = process_date(text)
    else:
        date = ''
    return date

def process_date(date):
    date = ' '.join(date.split()[-2:])      # Get the last two words - the closing date and time
    date = date.replace('.', '').upper()    # Converting the p.m. into an easily parsed format

    # If the html has changed this is where the code will likely break
    try:
        date_obj = datetime.datetime.strptime(date, "%d/%m/%Y %I:%M%p")
    except:
        print("Could not read date in Christchurch data")
        print(date)
        import sys; sys.exit()

    return date_obj
