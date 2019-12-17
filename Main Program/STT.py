
import json, pygame, time, wave, uuid
from ibm_watson import TextToSpeechV1, SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource
from mutagen.mp3 import MP3
'''
service = SpeechToTextV1(authenticator=IAMAuthenticator('-xtNqVhNOEOAaqMQfr9fY481ly7VsbL_ye4ToJahf_2o'))

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))
        for script in data['results'][0]['alternatives']:
            print(script['transcript'])

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

stt_callback = MyRecognizeCallback()

with open('1.mp3', 'rb') as file:
    audio = AudioSource(file)
    service.recognize_using_websocket(
        audio=audio, content_type='audio/mp3',
        model='ko-KR_BroadbandModel',
        recognize_callback=stt_callback,
        keywords=['노란선'],
        keywords_threshold=0.5,
        max_alternatives =3
    )

'''
service = TextToSpeechV1(authenticator=IAMAuthenticator('Yos_RquYkY8HfxshW4FFqNFkzuIZPPX4UTxvMAqSBZnM'))
service.set_service_url('https://gateway-seo.watsonplatform.net/text-to-speech/api')


voices = service.list_voices().get_result()
print('start')
#print(json.dumps(voices, indent=2)
pygame.init()
pygame.mixer.init()

pygame.display.set_mode((1,1))

scripts = [
    '지금, 설화명곡, 설화명곡',
    '설화명곡행 열차가 들어오고 있습니다',
    '노란선 뒤로 물러나 주시길 바랍니다.',
]

for script in scripts:
    filename = 'mp3/' + script + '.mp3' #+ str(uuid.uuid4())
    
    with open(filename, 'wb') as file:
        res = service.synthesize(script
        , accept='audio/mp3', voice="yuna").get_result()
        file.write(res.content)
        file.close()
    print('load end')
    audio = MP3(filename)



    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    print('play end', audio.info.length)
    
    time.sleep(audio.info.length)
    print('end')
pygame.mixer.quit()
pygame.quit()
 

