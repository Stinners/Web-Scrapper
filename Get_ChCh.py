# Currently just returning an empty feild for extra infro for Chch
# getting this will require following the link to each individual
# consultation page and extracting the text from there

# Note in general returning an empty string means the receiving
# function will ignore the output


from utilities import get_html, add_elem
# - get_html retreives htm from an address and returns it as a soup
# - add_elem takes a list and an element and adds the element to the
#    list if non empty, this is used when searches could return blank feilds

chch_adress = "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo/"

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
        date = text
    else:
        date = ''
    return date

# Main Block

def christchurch():
    try:
        soup = get_html(chch_adress)
    except ValueError:
        return("Invalid Adress: Christchurch")
    table = soup.find("table").find_all("td")
    names = []; links = []; info = []; dates = []

    for row in table:
        names = add_elem(names, get_name(row))
        links = add_elem(links, get_link(row))
        dates = add_elem(dates, get_date(row))
    consults = [[names[i], links[i], dates[i], "", []] for i in range(len(names))]
    return(consults)
