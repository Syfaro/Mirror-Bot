import praw
import redis


class RedditHandler:

    def __init__(self, user_agent='Pr0n mirror bot by /u/Syfaro'):
        self.reddit = praw.Reddit(user_agent=user_agent)
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set_site_handler(self, handler):
        self.handler = handler

    def set_subreddit(self, subreddit):
        self.subreddit = subreddit

    def set_login(self, username, password):
        self.username = username
        self.reddit.login(username, password)

    def get_new_submissions(self):
        last_submission = self.redis.get('mirrorbot:%s' % self.subreddit)

        submissions = self.reddit.get_subreddit(
            self.subreddit).get_new(limit=100)

        if last_submission is None:
            return submissions

        new_submissions = []
        for submission in submissions:
            if submission.name == last_submission:
                return new_submissions

            new_submissions.append(submission)

    def has_made_comment(self, thing):
        flat_comments = praw.helpers.flatten_tree(thing['thing'].comments)

        for comment in flat_comments:
            if comment.author == self.username:
                return True

            return False

    def items_to_process(self):
        things = self.get_new_submissions()

        to_process = []
        for thing in things:
            link = self.handler(thing)
            if link is not None:
                item = {'thing': thing}

                if isinstance(link, dict):
                    item['link'] = link['link']
                    if 'author' in link:
                        item['author'] = link['author']

                    if 'title' in link:
                        item['title'] = link['title']

                    if 'source' in link:
                        item['source'] = link['source']
                else:
                    item['link'] = link

                to_process.append(item)

        return to_process

    def do_magic(self, imgur, to_process):
        for item in to_process:
            if self.has_made_comment(item):
                continue

            links = []
            if isinstance(item['link'], list):
                for link in item['link']:
                    response = imgur.upload_image_by_url(link)
                    links.append(response['data']['link'])
            else:
                response = imgur.upload_image_by_url(item['link'])
                links.append(response['data']['link'])

            links_formatted = ''
            for link in links:
                links_formatted += "* [%s](%s)" % (link, link)

            comment = "imgur mirror:\n\n%s\n" % (links_formatted)

            if 'title' in item:
                comment += "\nTitle: %s\n" % (item['title'])
            if 'author' in item:
                comment += "\nArtist: %s\n" % (item['author'])
            if 'source' in item:
                comment += "\nSource: [%s](%s)\n" % (item['source'],
                                                     item['source'])

            comment += "\n\n_I am a bot, please message me with any concerns!_"

            item.add_comment(comment)
