import pyttsx3


def tts_options(text: str, rate: int, voice: int, volume: float) -> int:
    '''
    TTS function that converts the provided text to speech and plays the audio,
    based on provided speech rate, voice sound, and volume

    :param text: String to be spoken 
    :param rate: Integer speech rate in words per minute, must be greater than 0
    :param voice: Integer determining selected voice from list, from 0 to 47 inclusive
    :param volume: Float determining volume of audio, from 0.0 to 1.0 inclusive
    :return: 0 on success, 1 on failure
    '''

    if rate <= 0:
        print("Rate must be greater than 0")
        return 1
    if voice < 0 or voice > 47:
        print("Voice not in range [0, 47]")
        return 1
    if volume < 0.0 or volume > 1.0:
        print("Volume not in range [0.0, 1.0]")
        return 1

    try:
        engine = pyttsx3.init()
        voices = list(engine.getProperty("voices"))
        engine.setProperty("voice", voices[voice].id)
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)
        engine.say(text)
        engine.runAndWait()
        return 0
    except ImportError:
        print("Requested driver not found")
        return 1
    except RuntimeError:
        print("Driver failed to initialize")
        return 1


def tts_default(text: str) -> None:
    '''
    TTS function that converts the provided text to speech and plays the audio,
    based on default speech options:

    rate: 200 wpm
    voice: 0 (male)
    volume: 1.0 (full)

    :param text: String to be spoken
    :return: None
    '''

    pyttsx3.speak(text)

