# A simple library for reading and writing YAML files

def tabs(text):
    """ Puts tabs arround a peice of text """
    if text == "":
        return text
    else:
        return '"' + text + '"'

def write_YAML(f, city, subs_list):
    """ Takes a file in write or append mode an writes the list of submissions
        as a JSON object named as the city """

    # Clojure to simplity line writing
    def writeln(text, N_tabs):
        whitespace = 4 * N_tabs * ' '
        f.write(whitespace + text + '\n')
        return 0

    # Write city name
    writeln(" - " + city, 0)

    for sub in subs_list:
        # Write the name of the submission
        sub_name = sub[0].replace(' ', '_')
        writeln(' - ' + sub_name, 1)

        # Write each of the feilds
        writeln("link : " + tabs(sub[1]), 2)
        writeln("date : " + tabs(sub[2]), 2)
        writeln("info : " + tabs(sub[3]), 2)
        writeln("tags : " + str(sub[4]), 2)

    return 0
