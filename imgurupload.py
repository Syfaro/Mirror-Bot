import requests
import base64


class ImgurUpload:
    endpoint = 'https://api.imgur.com/3/'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def make_request(self, method, verb='GET', params=None):
        """
        Makes a `verb` request to the imgur API to `method` with `params`.
        """

        headers = {'Authorization': 'Client-ID ' + self.client_id}

        if verb == 'GET':
            return requests.get(self.endpoint + method, data=params, 
                                headers=headers).json()
        else:
            return requests.post(self.endpoint + method, data=params,
                                 headers=headers).json()

    def upload_image_by_url(self, url, title=None, description=None):
        """
        Uploads an image to imgur using a url,
        optionally with a `title` and `description`.
        """

        image = requests.get(url).content

        encoded = base64.b64encode(image)

        params = {'image': encoded, 'type': 'base64',
                  'title': title, 'description': description}

        return self.make_request('image', 'POST', params)

    def upload_image_by_file(self, path, title=None, description=None):
        """
        Uploads an image to imgur using a file,
        optionally with a `title` and `description`.
        """

        file = None
        with open(path) as f:
            file = f.read()

        encoded = base64.b64encode(file)

        params = {'image': encoded, 'type': 'base64',
                  'title': title, 'description': description}

        return self.make_request('image', 'POST', params)
