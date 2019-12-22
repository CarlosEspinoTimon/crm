import base64
import random
import string

from google.cloud import storage
from flask import current_app as app


class Image():
    extensions = ['.jpeg', '.png']

    def __init__(self):
        self.client = storage.Client(app.config['GOOGLE_PROJECT'])
        self.bucket = self.client.bucket(app.config['GOOGLE_BUCKET'])
        self.stored_image_prefix = app.config['STORED_IMAGE_PREFIX']

    def upload(self, data, previous_stored_image=None):
        encoded_image, extension, content_type = self.process_photo_input(data)
        
        if extension not in self.extensions:
            raise Exception("Invalid format, image has to be in jpeg or png")
        
        if previous_stored_image:
            self.delete_image(previous_stored_image)

        random_name = ''.join(random.choices(string.ascii_letters +
            string.digits, k=16))
        
        blob = self.bucket.blob(random_name)
        blob.upload_from_string(
            base64.decodebytes(encoded_image.encode()),
            content_type=content_type
        )
        blob.make_public()
        url = blob.public_url

        return url

    def process_photo_input(self, data):
        image = data['photo'].get('str_image')
        extension = data['photo'].get('extension')
        content_type = 'image/{}'.format(extension[1:])
        return image, extension, content_type

    def delete_image(self, previous_stored_image):
        name = previous_stored_image.split(self.stored_image_prefix)[1]
        blob = self.bucket.blob(name)
        blob.delete()
