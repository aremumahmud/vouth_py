from flask import Flask, request, jsonify
from voice_identification import VoiceIdentification  # Assuming VoiceIdentification is implemented in voice_identification.py

app = Flask(__name__)

voice_id_system = VoiceIdentification()

@app.route('/enroll', methods=['POST'])
def enroll_user():
    data = request.get_json()
    user_id = data.get('user_id')
    audio_urls = data.get('audio_urls', [])

    if user_id and len(audio_urls) == 3:
        try:
            voice_id_system.enroll_user(user_id, audio_urls)
            return jsonify({'status': 'success', 'message': 'User enrolled successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request parameters'})

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    audio_url = data.get('audio_url')

    if audio_url:
        try:
            result = voice_id_system.authenticate_user(audio_url)
            
            user_id = result[0]
            confidence = result[1]
            
            if user_id:
                return jsonify({'status': 'success', 'user_id': user_id, 'message': 'Authentication successful'})
            else:
                return jsonify({'status': 'error', 'message': 'Authentication failed'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request parameters'})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # app.run(debug=True)
    print("Flask server has started!")  # Add this line to print a message to the console when the server starts
