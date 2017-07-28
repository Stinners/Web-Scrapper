# Note wellington has its submissions divided into two sections, 'featured submissions'
# Currenly this script seems to be working for the featured submissions, however the
# regular submissions seem to me missing links to individual feedback pages

from datetime import datetime
from utilities import get_html

# Adress of the main page with the list of submissions
well_adress = "http://wellington.govt.nz/have-your-say/consultations"

# prfeix to be applied to each of the links on the submission page to give the full
# url for the individual submission pages
domain = "http://wellington.govt.nz"

def wellington():

    try:
        soup = get_html(well_adress)
    except ValueError:
        return "Invalid Address: Wellington"

    consults = []
    subs_containers = soup.find_all("div", class_="feature")
    for sub in subs_containers:
        name = sub.find("h2").text.strip()
        date = parse_date(sub.find("p", class_="smaller").text)
        link = domain + sub.find("a").get("href")
        info = sub.find("div", class_="feature-content").find("p").text.strip()
        consults.append([name, link, date, info, []])
    return consults


def parse_date(date_string):
    # Interprets the date format presented in the featured consultations
    _, time, day, month, year = date_string.split()

    # Time part needs to be heavity processed to get in
    # into a form strptime can parse
    if time[0] != '1':
        time = "0" + time             # Zero pad the time
    time = time.replace("a.m.", "AM") # Make am/pm into a
    time = time.replace("p.m.", "PM") # strptime frendly format

    # Similarly may need to zero pad the day
    if len(day) is 1:
        day = "0" + day

    new_string = time + day + month + year
    try:
        end = datetime.strptime(new_string, "%I.%M%p%d%B%Y")
    except:
        print("Could not parse date from Wellington featured consultations")
        import sys; sys.exit()

    return end
