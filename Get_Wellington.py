# Note Wellington has a "featured consultation" that this script does't 
# retreive 

from utilities import get_html, add_elem, clean 

well_adress = "http://wellington.govt.nz/have-your-say/consultations"

def wellington():

    try:
        soup = get_html(well_adress)
    except ValueError: 
        return "Invalid Address: Wellington"

    consults = soup.find("table").find_all("td")
    names = []; dates = []
    for i, text in enumerate(consults):
        # retreiving the text out of the html tags and saving it 
        # each second line is the date of the preceding consultation
        if (i % 2) == 0:
            name = clean(text.text.strip())
            names.append(name)
        else:
            dates.append(text.text.strip())
    consults_list = [[names[i], [],  dates[i], []] for i in range(len(names))]
    return consults_list

