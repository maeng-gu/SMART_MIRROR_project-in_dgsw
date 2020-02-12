#!bin/python3
import speech_recognition as sr
import pyaudio

r = sr.Recognizer()
p = pyaudio.PyAudio()
target = 0
for i in range(5):
    data = p.get_device_info_by_host_api_device_index(0, i)
    if data['name'] == 'Realtek Audio USB: Audio (hw:1,0)':
        target = i

mic = sr.Microphone(device_index=target)

with mic as source:
    print('say!')
    audio = r.listen(source)
    print(audio)
p.terminate()

print('done')
