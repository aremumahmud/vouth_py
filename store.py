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
