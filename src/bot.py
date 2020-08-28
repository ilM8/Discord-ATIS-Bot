import get_atis
from gtts import gTTS

language = "en"

airport_icao = "LOWW"
information_spoken = "Hotel"
runways_dep = "3 4 and 2 9"
runways_arr = "1 6"
ils = "1 6"

atis_text = get_atis.get_atis(airport_icao, information_spoken, runways_dep, runways_arr, ils)


speech = gTTS(text=atis_text, lang=language, slow=False)

speech.save("ATIS.mp3")
