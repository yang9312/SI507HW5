from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import string
import nltk # uncomment line after you install nltk
from nltk.corpus import stopwords



## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Section 06
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def params_unique(baseurl, params_d):
    res = []
    for k in sorted(params_d.keys()):
        res.append("{}={}".format(k, params_d[k]))
    return baseurl + '?' + "&".join(res)

def get_from_twitter(name, num):
    baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    param = {}
    param["screen_name"] = name
    param["count"] = num
    unique_ident = params_unique(baseurl, params_d = param)
    if unique_ident in CACHE_DICTION:
        print("Fetching cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params=param, auth = auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


#Code for Part 1:Get Tweets
## step 1
parameter = {}
parameter["screen_name"] = username
parameter["count"] = num_tweets
base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
umsiresp = requests.get(base_url, params=parameter, auth = auth)
umsi = json.loads(umsiresp.text)

## sterp 2
fil = open("tweet.json", "w")
fil.write(json.dumps(umsi, indent=4))
fil.close()


#Code for Part 2:Analyze Tweets
## step 2: tokenize the words
result = get_from_twitter(username, num_tweets)
text_list = [i["text"] for i in result]
token = []
for i in text_list:
    token += nltk.word_tokenize(i)

## step 3: get a frequency distribution of the tokenized list
fd = nltk.FreqDist(token).items()

## step 4
### ignore any words that do not start with an alphabetic character [a-zA-Z]
token1 = []
for i in token:
    if i[0] in string.ascii_letters:
        token1.append(i)

### ignore 'http', 'https', and 'RT'
token2 = []
for i in token1:
    if i != "http":
        if i != "https":
            if i != "RT":
                token2.append(i)

### ignore stop words
stopwords_list = list(set(stopwords.words('english')))
token3 = []
for i in token2:
    if i not in stopwords_list:
        token3.append(i)

## step 5:
# include stop words
new1 = nltk.FreqDist(token2).items()
commonwords1 = sorted(new1, key = lambda x : x[1], reverse = True)
feedback1 = "\nUSER: " + username + " TWEETS ANALYZED: " + num_tweets + " 5 MOST FREQUENT WORDS:"
for i in commonwords1[0:5]:
    feedback1 += i[0] + "(" + str(i[1]) + ") "
print(feedback1)
#ignore stop words
new2 = nltk.FreqDist(token3).items()
commonwords2 = sorted(new2, key = lambda x : x[1], reverse = True)
feedback2 = "\nUSER: " + username + " TWEETS ANALYZED: " + num_tweets + " 5 MOST FREQUENT WORDS (IGNORED STOP WORDS):"
for i in commonwords2[0:5]:
    feedback2 += i[0] + "(" + str(i[1]) + ") "
print(feedback2)

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
