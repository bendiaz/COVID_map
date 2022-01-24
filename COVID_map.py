import pandas
import folium
folmap = folium.Map(location=[34.06112803699629, -118.24010772157081],zoom_start=3,tiles="Stamen Terrain")
fg = folium.FeatureGroup(name="COVID 19")
 
covid_url =  "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
data = pandas.read_csv(covid_url)
dateRep = list(data["dateRep"])
cases = list(data["cases"])
deaths = list(data["deaths"])
countriesAndTerritories = list(data["countriesAndTerritories"])



##problems with names in opendata CSV, need to remove '_'
countriesAndTerritories = list(map(lambda item: item.replace("_"," "), countriesAndTerritories))
countriesAndTerritories = list(map(lambda item: item.replace(" of America",""), countriesAndTerritories))
# country_url = "https://github.com/google/dspl/blob/master/samples/google/canonical/countries.csv" 
data_cords = pandas.read_csv("mapping/countries.csv" )
country_names = data_cords.set_index("name")
 
all_cities = []
all_cases = []
all_deaths = []
all_cords = []
temp_death = 0
temp_case = 0
temp_ter = "first_itr"
for itdates, itcases, itdeaths, territories in zip(dateRep,cases,deaths,countriesAndTerritories):
    if temp_ter == territories:
        temp_death = temp_death + itdeaths
        temp_case = temp_case + itcases
    elif temp_ter != "first_itr":
        all_cities.append(temp_ter)
        all_cases.append(temp_case)
        all_deaths.append(temp_death)
        temp_ter = territories
        temp_death = 0
        temp_case = 0
        temp_death = temp_death + itdeaths
        temp_case = temp_case + itcases
    else:
        temp_ter = territories
        temp_death = temp_death + itdeaths
        temp_case = temp_case + itcases
 
for app_ter, app_cases ,app_deaths in zip(all_cities,all_cases,all_deaths):
    try:
    # if app_ter != "Curaçao" and app_ter !="Turks_and_Caicos_islands" and app_ter !="Antigua_and_Barbuda":
        if float(app_cases) < 15000:
            clr = 'green'
        elif float(app_cases) >= 15000 and float(app_cases) < 50000:
            clr = 'orange'
        else:
            clr = 'red'
        temp_cordi = list(country_names.loc[app_ter])
        temp_lat = float(temp_cordi[1])
        temp_lon = float(temp_cordi[2])
        fg.add_child(folium.Marker(location=[temp_lat,temp_lon], popup=str(app_ter)+" \n Cases: " 
        +str(app_cases)+ "\n Deaths : "
        +str(app_deaths),
        icon=folium.Icon(color=clr)))
    except KeyError:
        continue
 
folmap.add_child(fg)
folmap.add_child(folium.LayerControl())
folmap.save("mapping/covid.html")