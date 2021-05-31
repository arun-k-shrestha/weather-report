import collections
import requests

tuple_location = collections.namedtuple('tuple_location', 'city state country')
tuple_weather = collections.namedtuple('tuple_weather', 'tuple_location units temp condition')


def main():
    header()
    input_location = input("Enter your location - (Ex: Seattle, WA, US) ")
    loc = convert_location(input_location)
    weather = weather_api(loc)
    if not weather:
        print(f'\nNo weather report found for {input_location.upper()}!! \n')
        return
    
    report_weather(loc, weather)

def report_weather(loc, weather):
    scale = convert_scale(weather) 
    print(f'\nThe temperature in {location_name(loc)} is {weather.temp} {scale} and {weather.condition}. Enjoy your day. \n')

def convert_scale(weather):
    if weather.units == 'imperial':
        scale = 'F'
    else:
        scale = 'C'
    return scale

def location_name(location):
    if not location.state:
        return f'{location.city.title()}, {location.country.upper()}'
    else:
        return f'{location.city.title()}, {location.state.upper()}, {location.country.upper()}'


def weather_api(loc):
    url = f'https://weather.talkpython.fm/api/weather?city={loc.city}&country={loc.country}&units=imperial'
    if loc.state:
        url += f'&state={loc.state}'

    res = requests.get(url)
    if res.status_code in {400, 404, 500}:
        return None

    data = res.json()
    return convert_api(data, loc)


def convert_api(data, loc):
    temp = data.get('forecast').get('temp')
    w = data.get('weather')
    condition = f"has {w.get('description').lower()}"
    weather = tuple_weather(loc, data.get('units'), temp, condition)
    return weather


def convert_location(input_location):
    if not input_location or not input_location.strip():
        return None
    input_location = input_location.lower().strip()
    slipted_location = input_location.split(',')

    city = ""
    state = ""
    country = "US"

    if len(slipted_location) == 1:
        city = slipted_location[0].strip()
    elif len(slipted_location) == 2:
        city = slipted_location[0].strip()
        state = slipted_location[1].strip()
    elif len(slipted_location) == 3:
        city = slipted_location[0].strip()
        state = slipted_location[1].strip()
        country = slipted_location[2].strip()
    else:
        return None

    return tuple_location(city, state, country)


def header():
    print('********************************************************************************* \n')
    print('                               WEATHER REPORT                                     \n')
    print('********************************************************************************* \n')

main()
