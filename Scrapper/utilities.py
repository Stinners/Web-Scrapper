import urllib.request as urllib
from bs4 import BeautifulSoup

def get_html(adress):
    """ Gets HTML from the adress provided
    and returns it as a soup """
    response = urllib.urlopen(adress)   # add exception handeling to this
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return(soup)

def get_text(tag):
    """ Returns all the text in as soup that
    is between the tags provided """
    lines = []
    for tag in tags:
        line = tag.get_text()
        if line != '':
            line = line.strip('\n')
            lines.append(line)
    return(lines)

def add_elem(array, elem):
    """ Adds an element to a list if non empty
    used when searches could return blank feilds"""
    if elem != '':
        array.append(elem)
    return(array)

def clean(text):
    """ Removes all the special characters from a string"""
    special = "\n\t"
    # remove while space and special characters at the begining
    # and end of the string
    text = text.strip()
    new_text = ""
    special_chars = False
    # remove special characters in the interiour of the string and replace
    # with a space
    for letter in text:
        letter_is_special = letter in special

        if letter_is_special and not special_chars:
            new_text += " "
            special_chars = True
        elif not letter_is_special:
            new_text += letter
            special_chars = False

    return new_text

def tag_submissions(sub_list, tag_name, tag_keys):
    """ Reads through a list of submissions and adds the tag 'tag_name'
        if any of the strings, in 'tag_keys' are found in the the name or
        other information. Case insensitive """
    tag_name = tag_name.lower()
    for sub in sub_list:
        sub_name = sub[0].lower()
        extra_info = sub[3].lower()

        for key in tag_keys:
            key = key.lower()
            if (key in sub_name or key in extra_info):
                sub[4].append(tag_name)
                break

    return sub_list

def check_size(sub):
    """ Checks that the size of the strings in the submission is not to big
        for the models in Django """
    name_size = 200
    city_size = 50
    link_size = 250
    tag_size = 50

    fits = True
    fits *= name_size >= len(sub[0])
    fits *= link_size >= len(sub[1])
    for tag in sub[4]:
        fits *= tag_size > len(tag)

    if not fits:
        print("Submission is too big")
        print(sub)
        import sys; sys.exit()
