import folium
import geopy


def read_file(path, year, pointers=10):
    '''
    str, int, int -> dictionary
    path to the file
    year of the movies production
    max number of pointers you want to see on th map
    A function reading a file
    Returns dictionary, where keys are locations and values are movies
    '''
    d = {}
    file = open(path, 'r')
    for line in file:
        if len(d) == pointers + 5:
            return d
        if str(year) in line:
            line = line.split('\t')
            if line[-1].startswith('('):
                del line[-1]
            try:
                d[line[-1].strip()] += [line[0].split()[:-1]]
            except KeyError:
                d[line[-1].strip()] = [line[0].split()[:-1]]
    return d


def make_map(di):
    '''
    dictionary -> None
    A function creating a map with 3 layers
    '''
    mapp = folium.Map(zoom_start=6)
    fg1 = folium.FeatureGroup(name="Locations")
    fg2 = folium.FeatureGroup(name="Movies")
    fg3 = folium.FeatureGroup(name="Area")
    for key in di:
        tn = geopy.Nominatim(timeout=3).geocode(key)
        try:
            lt = tn.latitude
            ln = tn.longitude
            fg1.add_child(folium.CircleMarker(location=[lt, ln],
                                              radius=10,
                                              popup=key,
                                              color='red',
                                              fill_opacity=0.5))
            name = ''
            for e in di[key]:
                y = ' '.join(e)
                if "'" in y:
                    y = y.replace("'", "*")
                name += y
                name += ', '
            fg2.add_child(folium.Marker(location=[lt, ln],
                                        popup=name[:-2],
                                        icon=folium.Icon()))

            fg3.add_child(folium.GeoJson(data=open('world.json', 'r',
                                        encoding='utf-8-sig').read(),
                                        style_function=lambda x: {'fillColor': 'white'
                                        if x['properties']['AREA'] < 1000
                                         else 'blue' if 1000 <= x['properties']['AREA'] < 100000
                                         else 'green' if 100000 <= x['properties']['AREA'] < 1000000
                                         else 'purple'}))
        except AttributeError:
            continue

    mapp.add_child(fg1)
    mapp.add_child(fg2)
    mapp.add_child(fg3)
    mapp.add_child(folium.LayerControl())
    mapp.save("Map_movies.html")


make_map(read_file('locations.list', 2017))
