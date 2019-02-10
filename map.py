import folium
import csv

def read_file(year):
    '''
    Read file with film locations and parse it by string.
    Return dictionary with keys 'name', 'adress', 'inf' for films made in specified year.
    :param year: string
    :return: dict
    '''
    final_dict = dict()
    name_l = []
    adr_l = []
    inf_l = []
    with open('demo.list', 'r', encoding="utf-8", errors="ignore") as f:
        for i in range(14):
            next(f)
        reader = csv.reader(f, delimiter='\t')

        if len(name_l) != 10:
            for line in reader:
                try:
                    for i in range(3):
                        for el in line:
                            if el == '' or el == '\t' or el == "''":
                                line.remove(el)
                    line[0] = line[0].replace('{', '|').replace('}', '|').split('|')
                    for i in line[0]:
                        if i == '':
                            line[0].remove(i)
                    for i in range(len(line[0])):
                        if '#' in line[0][0]:
                            line[0][0] = line[0][0].replace('#', '')
                    line[0][0] = line[0][0].replace('#', '')
                    first = line[0]
                    line.remove(line[0])
                    temp_dat = ''
                    temp_dat = first[0][first[0].index('(') + 1: first[0].index(')')]
                    first[0] = first[0][:first[0].index('(')]

                    line.insert(0, first[0])
                    line.insert(0, temp_dat)

                    first.remove(first[0])
                    if first:
                        line.insert(3, first[0])
                    if line[0] == year:
                        name_l.append(line[1])
                        adr_l.append(line[2])
                        try:
                            if '#' in line[3]:
                                inf_l.append(line[3])
                            else:
                                inf_l.append('-')
                        except IndexError:
                            inf_l.append('-')
                except ValueError:
                    pass

            final_dict['name'] = name_l
            final_dict['adress'] = adr_l
            final_dict['inf'] = inf_l


    if len(name_l) == 0:
        print("Sorry, but there is no no film with this year.\nReload the program to restart.")
        return 2
    return final_dict


def localization(dict_loc):
    '''
    Finds location latitude and longitude for every film by its address in dictionary.
    Return updated dictionary with a new key add_loc.
    :param dict_loc: dict
    :return: dict
    '''
    print("Wait, please, the magic is in the air... It may take few minutes.")
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent='ma_name_anna', timeout=10, scheme='http')
    from geopy.extra.rate_limiter import RateLimiter
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    adr_list = []
    for point in dict_loc['adress']:
        try:
            location = geolocator.geocode(point)
            adr_list.append([location.latitude, location.longitude])
        except AttributeError:
            pass
    dict_loc['add_loc'] = adr_list
    return dict_loc

def countries_for_circle(final_dict2):
    '''
    Finds information of made films for countries user wants to compare.
    Return list of lists of country name user wrote, number of films and coordinates in tuple.
    :param final_dict2:
    :return: list
    '''
    countries = input("Now enter three countries you want to compare (space separated)(e.g. France Greece Denmark): ")
    countries = countries.split(' ')

    big_list = []
    if len(countries) == 3:
        for i in countries:
            number = 0
            for adr in final_dict2['adress']:
                if i.lower() in adr.lower():
                    number += 1
            big_list.append([i, number])

        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent='my_name_is_anna', timeout=10, scheme='http')
        from geopy.extra.rate_limiter import RateLimiter
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        for point in range(3):
            adr_list = []
            location = geolocator.geocode(countries[point])
            adr_list = location.latitude, location.longitude
            big_list[point].append(adr_list)
        return big_list
    else:
        print("Sorry, but the number of countries is not right.\nRestart the programm to try again.")
        return None

def color_creator(countries_list, num):
    '''
    Generate the color by comparing numbers of films in each country.
    Return 'red' if there is the biggest number, 'yellow' if it is middle, 'green' if it is the smallest.
    :param countries_list: list
    :param num: int
    :return: string
    '''
    if num == 0:
        if countries_list[0][1] >= countries_list[1][1]:
            if countries_list[0][1] >= countries_list[2][1]:
                return "red"
            elif countries_list[0][1] <= countries_list[2][1]:
                return "yellow"
        elif countries_list[0][1] >= countries_list[2][1]:
            if countries_list[0][1] >= countries_list[1][1]:
                return "red"
            elif countries_list[0][1] <= countries_list[1][1]:
                return "yellow"
        else:
            return "green"

    if num == 1:
        if countries_list[1][1] >= countries_list[0][1]:
            if countries_list[1][1] >= countries_list[2][1]:
                return "red"
            elif countries_list[1][1] <= countries_list[2][1]:
                return "yellow"
        elif countries_list[1][1] >= countries_list[2][1]:
            if countries_list[1][1] >= countries_list[0][1]:
                return "red"
            elif countries_list[1][1] <= countries_list[0][1]:
                return "yellow"
        else:
            return "green"

    if num == 2:
        if countries_list[2][1] >= countries_list[0][1]:
            if countries_list[2][1] >= countries_list[1][1]:
                return "red"
            elif countries_list[2][1] <= countries_list[1][1]:
                return "yellow"

        elif countries_list[2][1] >= countries_list[1][1]:
            if countries_list[2][1] >= countries_list[0][1]:
                return "red"
            elif countries_list[2][1] <= countries_list[0][1]:
                return "yellow"
        else:
            return "green"


def make_map(year, data, countries):
    '''
    Generate map from all the information.
    First layer - map.
    Second layer - locations with films names.
    Third layer - circle markers with amount of films in 3 countries.
    :param year: string
    :param data: string
    :param countries: list
    :return: None
    '''
    name = data['name']
    adress = data['add_loc']
    info = data['inf']
    map = folium.Map(location=adress[0],
                     tiles="Stamen Toner",
                     zoom_start=4)

    fg = folium.FeatureGroup(name="{} films".format(year))
    for i in range(len(name)):
        try:
            fg.add_child(folium.Marker(location=adress[i],
                                       popup=('Film: "{}"'.format(name[i])) + '(inf: {})'.format(info[i]),
                                       icon=folium.Icon()))
        except IndexError:
            pass

    fg_num = folium.FeatureGroup(name="Rating by countries")
    for num in range(3):
        fg_num.add_child(folium.CircleMarker(location=[countries[num][2][0], countries[num][2][1]],
                                         radius=30,
                                         popup=str(countries[num][0])+"\n"+" - {} films".format(str(countries[num][1])),
                                         fill_color=color_creator(countries, num),
                                         color='white',
                                         fill_opacity=0.5))

    map.add_child(fg)
    map.add_child(fg_num)
    map.add_child(folium.LayerControl())
    map.save('my_map3.html')


if __name__ == "__main__":
    the_year = input("Please, enter the year of films-making to generate a map (e.g. 2007): ")
    final_dict1 = read_file(the_year)
    if final_dict1 == 2:
        print()
    else:
        final_dict2 = localization(final_dict1)
        countries = countries_for_circle(final_dict2)
        make_map(the_year, final_dict2, countries)
        print("Check your folder! The process is finished! ")
