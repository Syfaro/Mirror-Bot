import requests
import re


def tumblr(thing, config):
    """
    handler for tumblr.com
    """

    key = config['keys']['id']

    blog = thing.true_domain

    post_id = re.search(r"\d+(?!\m)", thing.url).group(0)

    api_url = '''http://api.tumblr.com/v2/blog/{0}/posts/
                    photo?id={1}&api_key={2}'''.format(blog, post_id, key)

    post = requests.get(api_url).json()

    img = len(post['response']['posts'][0]['photos'])

    if img == 1:

        response = {'link': post['response']['posts'][0]['photos'][0]\
                    ['alt_sizes'][0]['url'], 'source': thing.url,
                     'author': post['response']['blog']['name']}

        return response

    else:
        response = {'is_album': True, 'source': thing.url, 
                    'author': post['response']['blog']['name'], 'link': []}

        for l in range(img):

            response['link'].append(post['response']['posts'][0]\
                                        ['photos'][l]['alt_sizes'][0]['url'])

        return response
