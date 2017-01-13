# Note wellington has its submissions divided into two sections, 'featured submissions'
# Currenly this script seems to be working for the featured submissions, however the
# regular submissions seem to me missing links to individual feedback pages

from datetime import datetime
from utilities import get_html, add_elem, clean

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

    names = []; dates = []
    links = []; info = []
    # Get the featured consultations
    featured = soup.findAll("div", {"class": "feature"})
    for div in featured:
        content = div.find('a')
        # Account for the fact that some links point to other WCC pages and
        # some go to survey monkey pages
        links.append(make_link(content.get('href')))
        date_string = content.find("div", {"class": "feature-date"}).text
        dates.append(parse_date(date_string))
        names.append(content.find('h2').text)
        info.append(content.findAll('p')[1].text)

    # This gets the non-featured consultations
    # Note: are these missing links?
    tables = soup.find("table")
    if tables != None:
        consults = tables.find_all("td")
        names = []; dates = []
        for i, text in enumerate(consults):
            # retreiving the text out of the html tags and saving it
            # each second line is the date of the preceding consultation
            if (i % 2) == 0:
                name = clean(text.text.strip())
                names.append(name)
                links.append("")
                info.append("")
            else:
                dates.append(text.text.strip())

    consults_list = [[names[i], links[i],  dates[i], info[i], []] for i in range(len(names))]

    # return an empty list if there are not open consultations other than the featured one
    return consults_list

def make_link(href):
    if href.startswith("http"):
        return href
    else:
        return domain + href


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
