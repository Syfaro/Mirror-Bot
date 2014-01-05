import yaml
import sched
import time

from imgurupload import ImgurUpload
from reddithandler import RedditHandler
from sitehandler import SiteHandler

from handlers.e621 import e621 as e621_handler
from handlers.furaffinity import furaffinity as furaffinity_handler

with file('config.yaml') as f:
	config = yaml.load(f.read())

handlers = SiteHandler()
handlers.load_config(config['domains'])

handlers.add_handler('e621.net', e621_handler)
handlers.add_handler('furaffinity.net', furaffinity_handler)

imgur = ImgurUpload(config['imgur']['id'], config['imgur']['secret'])

reddit = RedditHandler()
reddit.set_site_handler(handlers.run_handler)

s = sched.scheduler(time.time, time.sleep)

print 'Starting MirrorBot'

def process_accounts(sc):
	for subreddit in config['reddit']['subreddits']:
		print 'Updating %s with account %s' % (subreddit['subreddit'], subreddit['account'])
		reddit.set_subreddit(subreddit['subreddit'])
		reddit.set_login(subreddit['account'], config['reddit']['accounts'][subreddit['account']])
		print 'Authenticated as %s, starting checks' % subreddit['account']

		items = reddit.items_to_process()
		reddit.do_magic(imgur, items)
		print 'Finished %s' % (subreddit['subreddit'])

	sc.enter(60 * 5, 1, process_accounts, (sc, ))

s.enter(1, 1, process_accounts, (s, ))
s.run()