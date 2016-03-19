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
    """ Adds an element to a list of non empty 
    used when searches could return blank feilds"""
    if elem != '':
        array.append(elem)
    return(array)

def clean(text):
    """ Removes all the sepecial characters from a string"""
    special = "\n\t\t "
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


