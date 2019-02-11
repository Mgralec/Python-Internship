import csv, sys, pycountry, datetime


def change_date_format(date):
    date = datetime.datetime.strptime(item[index], '%m/%d/%Y').strftime('%Y-%m-%d')
    return date


def get_country_code(subdivision_name):
    #Function loops through subdivisions and countries in order to find matching country codes which are consisted of two characters.
    #If it finds it it returns three character country code, if not 'XXX'.

    for subdivision in pycountry.subdivisions:
        if subdivision_name == str(subdivision.name):
            for country in pycountry.countries:
                if str(country.alpha_2) == str(subdivision.country_code):
                    return country.alpha_3
    return 'XXX'


def count_ctr(impressions, percentage):
    # Function calculates CTR(click to impression rate) based on number of impressions and percentage.
    impressions = int(impressions)
    percentage = float(percentage.replace('%', '')) / 100
    clicks = int((percentage * impressions))
    clicks = round(clicks)

    return clicks

try:
    # Script checks if the file exists and can be opened.
    with open(sys.argv[1], encoding="utf8") as file:
        try:
            #Checking if the opened file is in CSV format. It returns dialect out of a sample from the file
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
        except csv.Error as csv_error:
            print('File probably not in CSV format')

        file_name = sys.argv[1]
        file_name = file_name.strip('.csv')
        reader = csv.reader(file)
        list_of_rows = list(reader)
        date = 0
        subdivision = 1
        no_of_impressions = 2
        no_of_clicks = 3

        for item in list_of_rows:
            for index, element in enumerate(item):
                #For each 'column' in a row I run separate function based on index value.
                if index == date:
                    try:
                        item[index] = change_date_format(item[index])
                    except ValueError:
                        print('Incorrect date format.')
                elif index == subdivision:
                    if isinstance(item[index], str):

                        item[index] = get_country_code(item[index])

                elif index == no_of_clicks:
                    try:
                        item[index] = count_ctr(item[no_of_impressions], item[index])
                    except ValueError:
                        print('Incorrect percentage format')

        list_of_rows.sort(key=lambda x: (x[date], x[subdivision]))
        #Sorting after date and subdivision using lambda function


        if list_of_rows:
            #If list not empty script writes into new file. Name created based on input file name

            new_file = open(file_name + '_processed_file.csv', 'w', encoding='utf8', newline='\n')

            with new_file:
                writer = csv.writer(new_file, dialect='excel')
                writer.writerows(list_of_rows)





except IOError as io_error:
    print(io_error)






