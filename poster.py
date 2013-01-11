import praw
import json
import urllib

REDDIT_USERNAME = ''
REDDIT_PASSWORD = ''

def main():

    #Load an RSS feed of the Hacker News homepage.
    url = "http://api.ihackernews.com/page"
    try:
        result = json.load(urllib.urlopen(url))
    except Exception, e:
        return
    
    items = result['items'][:-1]

    #Log in to Reddit
    reddit = praw.Reddit(user_agent='HackerNews bot by /u/cetamega')
    reddit.login(REDDIT_USERNAME, REDDIT_PASSWORD)

    link_submitted = False
    for link in items:
        if link_submitted:
            return
        try:
            #Check to make sure the post is a link and not a post to another HN page. 
            if not 'item?id=' in link['url'] and not '/comments/' in link['url']:
                submission = list(reddit.info(url=str(link['url'])))
                if not submission:
                    print "Submitting link: %s" % link['url']
                    subreddit = get_subreddit(str(link['title']))
                    resp = reddit.submit(subreddit, str(link['title']), url=str(link['url']))
                    link_submitted = True

        except Exception, e:
            print e
            pass

def get_subreddit(original_title):

    title = original_title.lower()

    apple = ['osx', 'apple', 'macintosh', 'steve jobs', 'woz']
    python = ['python', 'pycon', 'guido van rossum']
    webdev = ['.js', 'javascript', 'jquery']
    linux = ['linux', 'debian', 'redhat', 'linus', 'torvalds']
    programming = ['c++', 'programm', '.js', 'javascript', 'jquery', 'ruby']
    gaming = ['playstation', 'xbox', 'wii', 'nintendo']

    for word in apple:
        if word in title:
            return 'apple'

    for word in python:
        if word in title:
            return 'python'

    for word in webdev:
        if word in title:
            return 'webdev'

    for word in linux:
        if word in title:
            return 'linux'

    for word in programming:
        if word in title:
            return 'programming'

    for word in gaming:
        if word in title:
            return 'gaming'

    return 'technology'
    
if __name__ == "__main__":
    main()
