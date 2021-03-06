import yaml
import sched
import time
import warnings

from imgurupload import ImgurUpload
from reddithandler import RedditHandler
from sitehandler import SiteHandler

with open('config.yaml') as f:
    config = yaml.load(f.read())

# file() is deprecated in python 3.x, so if using that, change to open()

from handlers.e621 import e621 as e621_handler
from handlers.furaffinity import furaffinity as furaffinity_handler
from handlers.tumblr import tumblr as tumblr_handler
from handlers.deviantart import deviantart as deviantart_handler

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)

handlers = SiteHandler()
handlers.load_config(config['domains'])

handlers.add_handler('e621.net', e621_handler)
handlers.add_handler('furaffinity.net', furaffinity_handler)
handlers.add_handler('tumblr.com', tumblr_handler)
handlers.add_handler('deviantart.com', deviantart_handler)

imgur = ImgurUpload(config['imgur']['id'], config['imgur']['secret'])

reddit = RedditHandler()
reddit.set_site_handler(handlers.run_handler)

s = sched.scheduler(time.time, time.sleep)

print('Starting MirrorBot')


def process_accounts(sc):
    for subreddit in config['reddit']['subreddits']:
        print('Updating {0} with account {1}'.format(
                        subreddit['subreddit'], subreddit['account']))
        reddit.set_subreddit(subreddit['subreddit'])
        reddit.set_login(subreddit['account'], config['reddit']
                                ['accounts'][subreddit['account']])
        print('Authenticated as {}, starting checks'.format(
                                        subreddit['account']))

        items = reddit.items_to_process()
        if items is None:
            print('No new items in {}'.format(subreddit['subreddit']))
            continue
        reddit.do_magic(imgur, items)
        print('Finished {}'.format(subreddit['subreddit']))

    sc.enter(60 * 5, 1, process_accounts, (sc, ))

s.enter(1, 1, process_accounts, (s, ))
s.run()
