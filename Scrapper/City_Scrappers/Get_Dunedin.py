# Dunedin have an RSS feed for current consultations
# This may be an easier than manualy scraping data

from utilities import get_html, add_elem
import datetime


dunedin_adress = "http://www.dunedin.govt.nz/council-online/currently-consulting-on"

def read_table(table):
    subs = []
    """ Reads the submission data from a table"""
    tds = table.find_all('td')
    for i, td in enumerate(tds):
        if (i % 2) == 0:
            name = td.text
            link = td.find('a').get('href')
        else:
            date = td.text
            date = process_date(date)
            subs.append([name, link, date, "", [] ])
    return subs

def process_date(date):
    date = ' '.join(date.split()[-3:])
    try:
        date_obj = datetime.datetime.strptime(date,"%d/%m/%Y")
    except:
        import sys
        print("Cannot read date in Dunedin data")
        print(date)
        sys.exit()

    return date_obj

def dunedin():
    try:
        soup = get_html(dunedin_adress)
    except ValueError:
        return("Invalid Adress: Dunedin")

    # Get the tables in the site
    tables = soup.find_all('table')

    # The second table contains the currently opne submissions
    subs = read_table(tables[1])

    # The third table contains closed consultations
    # I'm not reading this for not but it has the same format and can be read by the same function

    return subs
