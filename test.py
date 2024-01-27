from voice_identification import VoiceIdentification  # Assuming VoiceIdentification is implemented in voice_identification.py

voice_id_system = VoiceIdentification()

audio_urls  = ["https://res.cloudinary.com/dvauarkh6/video/upload/v1706029656/audio/file.wav",
        "https://res.cloudinary.com/dvauarkh6/video/upload/v1706029749/audio/file.wav",
        "https://res.cloudinary.com/dvauarkh6/video/upload/v1706029791/audio/file.wav"]
voice_id_system.enroll_user('hehdnbfjmrb nfbnbnm ', audio_urls)


audio_url = "https://res.cloudinary.com/dvauarkh6/video/upload/v1706029656/audio/file.wav"
audio_url1 ='https://res.cloudinary.com/dvauarkh6/video/upload/v1706353198/audio/file.wav'
audio_url2 ='https://res.cloudinary.com/dvauarkh6/video/upload/v1706353444/audio/file.wav'
audio_url3 = 'https://res.cloudinary.com/dvauarkh6/video/upload/v1706353486/audio/file.wav'

result = voice_id_system.authenticate_user(audio_url1)
result1 = voice_id_system.authenticate_user(audio_url2)
result2 = voice_id_system.authenticate_user(audio_url3)
result3 = voice_id_system.authenticate_user(audio_url)

print(result, result1, result2 , result3)