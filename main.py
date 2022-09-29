import requests
import configparser

# assignment 1 - accuweather API
# David Rochon, Due Monday 9/26

#1. Ask the	user for the location
#2. Convert	the	location into a code
#3. Use	the	code to get the current conditions
#4. Use	the	code again to get the 5day forecast

# Include error handling

#Use factory pattern to generate url from one method
def get_url(api_key_from_config, url_type, loc_key):
    if(url_type == "location"):
        # ask user for a location
        location = input("Welcome to the Accuweather app! Please input a location (zip code): ")
        location_url = 'https://dataservice.accuweather.com/locations/v1/' \
                       'postalcodes/search?apikey={}&q={}'.format(api_key_from_config, location)
        return location_url
    elif(url_type == "conditions"):
        conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/' \
                         '{}?apikey={}'.format(loc_key, api_key_from_config)
        return conditions_url
    elif(url_type == "5day"):
        forecast_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' \
                       '{}?apikey={}'.format(loc_key, api_key_from_config)
        return forecast_url


#get apikey for url from config
#TODO: use VCS -> Share Project on Github, do not check in app.config, just template and main code
def get_apikey():
    config = configparser.ConfigParser()
    config.read('app.config')
    apikey_from_file = config['secrets']['apikey']
    #debug statement
    #print(apikey_from_file)
    return apikey_from_file

class NoSuchLocation(Exception):
    pass


def get_location(location_url):

    response = requests.get(location_url)

    #debugging statements
    #print(response)
    #print(response.status_code)
    #print(response.json())
    #print()
    #print(response.json()[0])
    #print()

    try:
        key = response.json()[0].get('Key')
        #print("Key is: " + key)
    except IndexError:
        raise NoSuchLocation()
    return key


def get_conditions(conditions_url):
    response = requests.get(conditions_url)

    #debugging statement
    #print(response.json())

    json_version = response.json()
    print("Current Conditions: {}\n".format(json_version[0].get('WeatherText')))
    #printing current temperature
    print("Current Temperature in Degrees Fahrenheit: {}\n".format(json_version[0].get('Temperature').get('Imperial')
                                                                   .get('Value')))

def get_five_day_forecast(forecast_url):

    #debugging statement
    #print("Forecast URL is: " + forecast_url)

    response = requests.get(forecast_url)
    #gets the json of the response (otherwise would get response status code if I'm not mistaken?)
    json_version = response.json()

    #debugging statement
    #print(json_version)

    #debugging statement to make sure "DailyForecasts" is printing correctly
    #print("Five Day Forecast is: {}".format(json_version.get('DailyForecasts')))

    #getting just the highs and lows for each of the five days (not all info)
    print("Your five day forecast: \n")
    for entry in json_version.get('DailyForecasts'):
        #print(entry)
        print("Date: {}".format(entry.get('Date')))
        print("Minimum Temperature in Degreees Fahrenheit: {}".format(entry.get('Temperature').get('Minimum')
                                                                      .get('Value')))
        print("Maximum Temperature in Degrees Fahrenheit: {}".format(entry.get('Temperature').get('Maximum')
                                                                     .get('Value')))


try:
    api_key = get_apikey()
    url = get_url(api_key, "location", 0)
    location_key = get_location(url)
    url = get_url(api_key, "conditions", location_key)
    get_conditions(url)
    url = get_url(api_key, "5day", location_key)
    get_five_day_forecast(url)
except NoSuchLocation:
    print("Unable to get the location")
