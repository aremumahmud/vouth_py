import os
import numpy as np
import requests
from io import BytesIO
import librosa
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib

class VoiceIdentification:
    def __init__(self, model_file="voice_id_model.joblib"):
        self.model_file = model_file
        self.users_data = {}  # Dictionary to store user data
        self.load_model()

    def enroll_user(self, user_id, audio_files):
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
            mel_spectrogram = librosa.feature.mfcc(y=y, sr=sr , n_mfcc=16)
            features = np.mean(mel_spectrogram, axis=1)  # Use mean of each row as a feature

            user_features.append(features)

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
        mel_spectrogram = librosa.feature.mfcc(y=y, sr=sr , n_mfcc=16)
        features = np.mean(mel_spectrogram, axis=1)
        print(features.shape)
        # Compare with enrolled users' data
        similarities = {}
        for user_id, enrolled_features in self.users_data.items():
            similarity = np.dot(features, enrolled_features) / (np.linalg.norm(features) * np.linalg.norm(enrolled_features))
            similarities[user_id] = similarity

        # Find the user with the highest similarity
        predicted_user = max(similarities, key=similarities.get)
        confidence = similarities[predicted_user]

        # Set a threshold for confidence
        threshold = 0.7
        print(confidence)
        if confidence > threshold:
            return [predicted_user, confidence]
        else:
            return [None , confidence]

    def save_model(self):
        joblib.dump(self.users_data, self.model_file)

    def load_model(self):
        if os.path.exists(self.model_file):
            self.users_data = joblib.load(self.model_file)

# Example usage: