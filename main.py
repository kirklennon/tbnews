# Import the Twython class
from twython import Twython
import json
import urllib

# Load credentials from json file
with open("/var/www/twitternews/credentials.json", "r") as file:
    creds = json.load(file)

pagebody = []

python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
query = {'q': 'video ("did you take this" OR "on all of our platforms" OR "can we have your permission" OR "did you shoot this" OR "irrevocable permission to share" OR "with full credits to you" OR "and its affiliates" OR "permission to use in perpetuity" OR "on all of our platforms" OR "with full credit to you" OR "can we use your video" OR "did you shoot this")',
        'result_type': 'latest',
        'count': 5,
        'lang': 'en',
        }
header = open('/var/www/twitternews/header.txt').read()
footer = open('/var/www/twitternews/footer.txt').read()
pagebody.append(header)
for status in python_tweets.search(**query)['statuses']:
	id = status['in_reply_to_status_id']
	if id is not None:
		url = 'https://twitter.com/anyuser/status/' + str(id)
		response = urllib.request.urlopen('https://publish.twitter.com/oembed?url='+url).read()
		data = json.loads(response)
		pagebody.append(data['html'][:-86])
pagebody.append(footer)

page = open('/var/www/html/news/index.html','w+')
page.writelines(pagebody)
page.close()