import BeautifulSoup
import praw
import json
import urllib

def main():

    url = "http://hndroidapi.appspot.com/news/format/json/page/?appid="
    result = json.load(urllib.urlopen(url))
    
    items = result['items'][:-1]

    """
    item_list = []
    for item in items:
        if 'score' in item:
            item['score'] = int(item['score'].split(' ')[0])
            if not item_list:
                item_list.append(item)
            else:
                if item['score'] > item_list[-1]['score']:
                    item_list.append(item)
    """

    reddit = praw.Reddit(user_agent='HackerNews bot by /u/cetamega')
    reddit.login('cetamega', 'Nuo4D%!Kt%$e')

    link_submitted = False
    for link in items:
        if link_submitted:
            return
        try:
            submission = list(reddit.info(url=str(link['url'])))
            if not submission:
                print "Submitting link: %s" % link['url']
                subreddit = get_subreddit(str(link['title']))
                resp = reddit.submit(subreddit, str(link['title']), url=str(link['url']))    
                link_submitted = True

        except Exception, e:
            print e
            pass

def get_subreddit(title):
    
    if 'osx' in title or 'apple' in title:
        return 'apple'
        
    if 'python' in title or 'pycon' in title:
        return 'python'    

    if 'C++' in title or 'programming' in title or 'programmer' in title:
        return 'programming'

    if 'playstation' in title or 'xbox' in title or 'wii' in title:
        return 'gaming'

    return 'technology'
    
if __name__ == "__main__":
    main()
