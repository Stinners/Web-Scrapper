# Currently just returning an empty feild for extra infro for Chch
# getting this will require following the link to each individual
# consultation page and extracting the text from there


from utilities import get_html, add_elem 

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

# Main Block 

def christchurch():
    soup = get_html(chch_adress)
    table = soup.find("table").find_all("td")
    names = []; links = []; info = [];

    for row in table:
        names = add_elem(names, get_name(row))
        links = add_elem(links, get_link(row))

    consults = [[names[i], links[i], []] for i in range(len(names))]
    return(consults)

