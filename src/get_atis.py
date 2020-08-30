from gtts import gTTS
import os
from urllib import request
from urllib import parse
import json
from dotenv import load_dotenv

airport_icao = "KJFK"
information_letter = "Golf"
runways_dep = "1 3 Right"
runways_arr = "1 3 Left"
ils = "1 3 Left"

load_dotenv()
AVWX_TOKEN = os.getenv('AVWX_TOKEN')

headers = {
    'Authorization': AVWX_TOKEN
}

def get_atis(airport_icao, information_spoken, runways_dep, runways_arr, ils):
    atis_json = request.Request(f'https://avwx.rest/api/metar/{airport_icao}?onfail=error', headers=headers)

    response = request.urlopen(atis_json).read()

    response = json.loads(response)
    print(response)

    altimeter = response["altimeter"]
    clouds = response["clouds"]
    flight_rules = response["flight_rules"]
    sanitized = response["sanitized"]
    wind_direction = response["wind_direction"]
    wind_speed = response["wind_speed"]
    visibility = response["visibility"]
    raw = response["raw"]
    dewpoint = response["dewpoint"]
    temperature = response["remarks_info"]["temperature_decimal"]
    if temperature == None:
        temperature = response["temperature"]
    time = response["time"]["dt"].split("T")[1].split(":")
    time = str(time[0] + time[1])
    time_spoken = ""
    for char in time:
        time_spoken += f"{char} "
    print(time_spoken)

    print(response)

    text = f"{airport_icao} Ay TIS information {information_spoken} . {time_spoken} zulu. visibility {visibility['spoken']}. temperature {temperature['spoken']}. dewpoint {dewpoint['spoken']}. altimeter {altimeter['spoken']}. winds {wind_direction['spoken']} at {wind_speed['spoken']}. I L S runway {ils} approach in use. landing runway {runways_arr}. depature runway {runways_dep}. VFR aircraft say direction of flight. Readback all runway hold short instructions. Advise controller on initial contact you have information {information_spoken}"
    print(text)
    """
    language = "en"

    speech = gTTS(text=text, lang=language, slow=False)

    speech.save("test.mp3")
    """

    return text

def get_raw_atis(airport_icao):
    atis_json = request.Request(f'https://avwx.rest/api/metar/{airport_icao}?onfail=error', headers=headers)

    response = request.urlopen(atis_json).read()

    response = json.loads(response)

    return response["raw"]
