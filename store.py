import requests
from io import BytesIO
import cloudinary
import cloudinary.uploader
import cloudinary.api

class CloudinaryUtils:
    def __init__(self, model_file="voice_id_model.joblib"):
        self.model_file = model_file

    def upload_model_to_cloudinary(self):
        # Save the model to Cloudinary
        cloudinary.uploader.upload(self.model_file, public_id="voice_id_model")

    def download_model_from_cloudinary(self):
        # Load the model from Cloudinary
        response = cloudinary.api.resource("voice_id_model", format="json")
        if response and 'url' in response:
            model_url = response['url']
            model_content = requests.get(model_url).content
            with open(self.model_file, 'wb') as local_file:
                local_file.write(model_content)
            return True
        else:
            print("Failed to load model from Cloudinary")
            return False

# End of cloudinary_utils.py
import os
import numpy as np
import requests
from io import BytesIO
import librosa
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import librosa.effects as effects
import joblib

class VoiceIdentification:
    def __init__(self, model_file="voice_id_model.joblib"):
        self.model_file = model_file
        self.users_data = {}  # Dictionary to store user data
        self.load_model()

    def enroll_user(self, user_id, audio_files, augmentation_factor=5):
        # Enroll a user by extracting features from their voice and storing the data
        user_features = []

        for audio_file in audio_files:

            response = requests.get(audio_file)
            if response.status_code == 200:
                audio_bytes = BytesIO(response.content)
                y, sr = librosa.load(audio_bytes)
            else:
                raise Exception(f"Failed to fetch audio from URL: {audio_file}")

            # Extract features (Mel spectrogram)
            mel_spectrogram = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=16)
            features = np.mean(mel_spectrogram, axis=1)  # Use mean of each row as a feature

            user_features.append(features)

        print('hello')
       # Data Augmentation
        for _ in range(augmentation_factor):
            # Apply pitch shift
            y_pitch_shifted = effects.pitch_shift(y,sr=sr, n_steps=2)
            augmented_mfccs = librosa.feature.mfcc(y=y_pitch_shifted, sr=sr, n_mfcc=16)
            
            augmented_features = np.mean(augmented_mfccs, axis=1, dtype=object)
            
            user_features.append(augmented_features)
        print('restock')
        
        
        # Ensure all elements have the same length and dtype
        max_length = max(len(arr) for arr in user_features)
        user_features = [np.pad(np.array(x, dtype=np.float32), (0, max_length - len(x))) for x in user_features]

        # print(user_features)
        # Store user data
        self.users_data[user_id] = np.mean(user_features, axis=0)
        self.save_model()

    def authenticate_user(self, audio_file):
        # Authenticate a user by comparing their voice features with enrolled users' data
        # Load audio file
        response = requests.get(audio_file)
        if response.status_code == 200:
            audio_bytes = BytesIO(response.content)
            y, sr = librosa.load(audio_bytes)
        else:
            raise Exception(f"Failed to fetch audio from URL: {audio_file}")

        # Extract features (Mel spectrogram)
        mel_spectrogram = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=16)
        features = np.mean(mel_spectrogram, axis=1,dtype=object)
        # print(features)
        # Compare with enrolled users' data
        similarities = {}
        for user_id, enrolled_features in self.users_data.items():

             # Ensure the enrolled features have the same length as the features
            enrolled_features = np.pad(enrolled_features, (0, len(features) - len(enrolled_features)))
        
            similarity = np.dot(features, enrolled_features) / (np.linalg.norm(features) * np.linalg.norm(enrolled_features))
            similarities[user_id] = similarity

        # Find the user with the highest similarity
        predicted_user = max(similarities, key=similarities.get)
        confidence = similarities[predicted_user]

        # Set a threshold for confidence
        threshold = 0.99993
        # print(confidence)
        if confidence > threshold:
            return [predicted_user , confidence]
        else:
            return None

    def save_model(self):
        joblib.dump(self.users_data, self.model_file)

    def load_model(self):
        if os.path.exists(self.model_file):
            self.users_data = joblib.load(self.model_file)

# Example usage:

