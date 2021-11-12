from django.test import TestCase
from twitter.models import *
import datetime
import threading

import json
    
def parse_date(tweet):
    tweet['created_at'] = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    tweet['user']['created_at'] = datetime.datetime.strptime(tweet['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    return tweet

def tweetParse(tweet):
    tweet = parse_date(tweet)

    if('retweeted_status' in tweet):
        retweeted_status = tweetParse(tweet.get('retweeted_status',False))
    else:
        retweeted_status = None

    if('quoted_status' in tweet):
        quoted_status = tweetParse(tweet.get('quoted_status',False))
    else:
        quoted_status = None

    user = User(
        id = tweet['user']['id_str'],
        name = tweet['user']['name'],
        screen_name = tweet['user']['screen_name'],
        location = tweet['user']['location'],
        description = tweet['user']['description'],
        protected = tweet['user']['protected'],
        followers_count = tweet['user']['followers_count'],
        fast_followers_count = tweet['user'].get('fast_followers_count',None),
        normal_followers_count = tweet['user'].get('normal_followers_count',None),
        friends_count = tweet['user']['friends_count'],
        listed_count = tweet['user']['listed_count'],
        created_at = tweet['user']['created_at'],
        favourites_count = tweet['user']['favourites_count'],
        geo_enabled = tweet['user']['geo_enabled'],
        verified = tweet['user']['verified'],
        statuses_count = tweet['user']['statuses_count'],
        media_count = tweet['user'].get('media_count',None),
        lang = tweet['user']['lang'],
        contributors_enabled = tweet['user']['contributors_enabled'],
        is_translator = tweet['user']['is_translator'],
        is_translation_enabled = tweet['user']['is_translation_enabled'],
        profile_background_color = tweet['user']['profile_background_color'],
        profile_background_image_url = tweet['user']['profile_background_image_url'],
        profile_background_image_url_https = tweet['user']['profile_background_image_url_https'],
        profile_background_tile = tweet['user']['profile_background_tile'],
        profile_image_url = tweet['user']['profile_image_url'],
        profile_image_url_https = tweet['user']['profile_image_url_https'],
        profile_banner_url = tweet['user'].get('profile_banner_url',None),
        profile_link_color = tweet['user']['profile_link_color'],
        profile_sidebar_border_color = tweet['user']['profile_sidebar_border_color'],
        profile_sidebar_fill_color = tweet['user']['profile_sidebar_fill_color'],
        profile_text_color = tweet['user']['profile_text_color'],
        profile_use_background_image = tweet['user']['profile_use_background_image'],
        has_custom_timelines = tweet['user'].get('has_custom_timelines',None),
        advertiser_account_type = tweet['user'].get('advertiser_account_type',None),
        analytics_type = tweet['user'].get('analytics_type',None),
        translator_type = tweet['user'].get('translator_type',None),
    )
    users_bulk[user.id] = user

    for url_json in tweet['user']['entities'].get('url',{'urls':[]})['urls']:
        url = Url(
            #id = url_json['url'],
            url = url_json['url'],
            expanded_url = url_json.get('expanded_url',None),
            display_url = url_json.get('display_url', None),
        )
        url_bulk[url.url] = url
        url_bulk_through[(url.url,user.id)] = User.urls.through(user_id=user.id,url_id=url.url)

        
    for description_url_json in tweet['user']['entities']['description']['urls']:
        url = Url(
            url = description_url_json['url'],
            expanded_url = description_url_json['expanded_url'],
            display_url = description_url_json['display_url'],
        )
        url_bulk[url.url] = url
        urlDescription_bulk_through[(url.url,user.id)] = User.descriptionUrl.through(user_id=user.id,url_id=url.url)

    status = Status(
        created_at = tweet['created_at'],
        id = tweet['id_str'],
        content = tweet['full_text'],
        display_text_range_start = tweet['display_text_range'][0],
        display_text_range_end = tweet['display_text_range'][1],
        user_id = user.id,
        source = tweet['source'],
        in_reply_to_status_id = tweet['in_reply_to_status_id'],
        in_reply_to_user_id = tweet['in_reply_to_user_id'],
        in_reply_to_screen_name = tweet['in_reply_to_screen_name'],
        #place = models.ForeignKey(Place,on_delete=models.PROTECT)
        is_quote_status = tweet['is_quote_status'],
        retweet_count = tweet['retweet_count'],
        favorite_count = tweet['favorite_count'],
        conversation_id = tweet.get('conversation_id',None),
        possibly_sensitive = tweet.get('possibly_sensitive',False),
        possibly_sensitive_editable = tweet.get('possibly_sensitive_editable',False),
        lang = tweet['lang'],
        retweet_status_id = None, #if retweeted_status == None else retweeted_status.id,
        quoted_status_id = None #if quoted_status == None else quoted_status.id,
    )
    status_bulk[status.id] = status

    if 'extended_entities' in tweet:
        for entity_json in tweet['extended_entities']['media']:
            if(entity_json['type'] == "photo"):
                url = Url(
                    url = entity_json['url'],
                    display_url = entity_json['display_url'],
                    expanded_url = entity_json['expanded_url'],
                )
                url_bulk[url.url] = url
                photo = Photo(
                    id = entity_json['id_str'],
                    media_url = entity_json['media_url'],
                    media_url_https = entity_json['media_url_https'],
                    media_key = entity_json.get('media_key',None),
                    url_id = url.url,
                )
                photos_bulk[photo.id] = photo
                photoStatus_bulk[(photo.id,status.id)] = Status.photos.through(photo_id=photo.id,status_id=status.id)

            elif(entity_json['type'] == "video"):
                url = Url(
                    url = entity_json['url'],
                    display_url = entity_json['display_url'],
                    expanded_url = entity_json['expanded_url'],
                )
                url_bulk[url.url] = url
                for variants_json in entity_json['video_info']['variants']:
                    if( variants_json["content_type"] == "application/x-mpegURL" ):
                        video_url = variants_json["url"]
                    
                video = Video(
                    id = entity_json['id_str'],
                    media_url = entity_json['media_url'],
                    media_url_https = entity_json['media_url_https'],
                    media_key = entity_json.get('media_key',None),
                    url_id = url.url,
                    aspect_ratio_x = entity_json['video_info']['aspect_ratio'][0],
                    aspect_ratio_y = entity_json['video_info']['aspect_ratio'][1],
                    duration_millis = entity_json['video_info']['duration_millis'],
                    video_url = video_url,
                )
                videos_bulk[video.id] = video
                videosStatus_bulk[(video.id,status.id)] = Status.videos.through(video_id=video.id,status_id=status.id)
            elif(entity_json['type'] == "animated_gif"):
                url = Url(
                    url = entity_json['url'],
                    display_url = entity_json['display_url'],
                    expanded_url = entity_json['expanded_url'],
                )
                url_bulk[url.url] = url
                gif = Gif(
                    id = entity_json['id_str'],
                    media_url = entity_json['media_url'],
                    media_url_https = entity_json['media_url_https'],
                    media_key = entity_json.get('media_key',None),
                    url_id = url.url,
                    aspect_ratio_x = entity_json['video_info']['aspect_ratio'][0],
                    aspect_ratio_y = entity_json['video_info']['aspect_ratio'][1],
                    gif_url = entity_json['video_info']['variants'][0]["url"],
                )
                gifs_bulk[gif.id] = gif
                gifsStatus_bulk[(gif.id,status.id)] = Status.gifs.through(gif_id=gif.id,status_id=status.id)


    for hashtag_json in tweet['entities']['hashtags']:
        hashtag = Hashtag(
            text = hashtag_json['text']
        )
        hashtag_bulk[hashtag.text] = hashtag
        hashtag_bulk_through[(hashtag.text,status.id)] = Status.hashtags.through(status_id=status.id,hashtag_id=hashtag.text)

    for user_mention_json in tweet['entities']['user_mentions']:
        user_mention = UserMention(
            screen_name = user_mention_json['screen_name'],
            name = user_mention_json['name'],
            id = user_mention_json['id_str'],
        )
        userMention_bulk[user_mention.id] = user_mention 
        userMention_bulk_through[(user_mention.id,status.id)] = Status.user_mentions.through(status_id=status.id,usermention_id=user_mention.id)

    for url_json in tweet['entities']['urls']:
        url = Url(
            url = url_json['url'],
            expanded_url = url_json['expanded_url'],
            display_url = url_json['display_url'],
        )
        url_bulk[url.url] = url
        urlStatus_bulk_through[(url.url,status.id)] = Status.urls.through(status_id=status.id,url_id=url.url)

    return Status


import tweepy
import json

class TwitterAPI:
    def __init__(self):
        self.keys = [
                    ['2m2IZIw55y8XMTRLep2gx6van','kcF8ZCrA6yK4zZFVkGYSkEd7W5sopi5GFjJoQLg1n75WA22Vlc'],
                    ]
                    
        self.apis = []
        for x in self.keys:
                auth = tweepy.AppAuthHandler(x[0], x[1]) 
                authenticated = tweepy.API(auth, wait_on_rate_limit=True)
                self.apis.append(authenticated)
           
    @property
    def keysLen(self,):
        return len(self.keys)

    def splitList(self,alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts) ]


class TwitterTimeLine(TwitterAPI):
    def __init__(self):
        super().__init__()
        self.data = {}

    def _getTweets(self,screen_names,api):
        for i,id in enumerate(screen_names):
            self.data[id] = []
            print(id)
            
            try:
                for x in tweepy.Cursor(api.user_timeline, screen_name=id,tweet_mode="extended",count=200).items():
                    self.data[id].append(x._json)
                    #tweet = parse_date(x._json)
                    #tweetParse(x._json)

                # handle = Handle.objects.get(handle=id)
                # handle.id = x._json['user']['id_str']
                # handle.save()

            except:
                print('except', id)
                continue

            with open('backup2/{}.json'.format(id), 'w',encoding='utf-8') as json_file:
                json.dump(self.data[id], json_file)
            self.data.pop(id,None)

    def getTweets(self, userids):
        splitedList = self.splitList(userids,self.keysLen)        
        threads = [threading.Thread(target=self._getTweets, args=(splitedList[i],self.apis[i])) for i in range(self.keysLen)]
        print(threads)
        [thread.start() for thread in threads]        
        [thread.join() for thread in threads]


from glob import glob

paths = glob('backup2/*.json')
print(paths)

users_bulk = {}
status_bulk = {}
url_bulk = {}
url_bulk_through = {}
urlDescription_bulk_through = {}
hashtag_bulk = {}
hashtag_bulk_through = {}
userMention_bulk = {}
userMention_bulk_through = {}
urlStatus_bulk_through = {}
photos_bulk = {}
photoStatus_bulk = {}
videos_bulk = {}
videosStatus_bulk = {}
gifs_bulk = {}
gifsStatus_bulk = {}

import gc
for i,path in enumerate(paths):
    with open(path, 'r') as f:
        # if(i < 23):
        #     continue
        print(f'{i} of {len(paths)}, file:{path}')
        try:
            tweets = json.load(f)
            
        except:
            continue

        for tweet in tweets:
            tweetParse(tweet)

        if( i%1 == 0 or i == len(paths)-1):
            print('writing')
            User.objects.bulk_create( list(users_bulk.values()) ,ignore_conflicts=True)
            Status.objects.bulk_create( list(status_bulk.values()) ,ignore_conflicts=True)
            Url.objects.bulk_create( list(url_bulk.values()) ,ignore_conflicts=True)
            Hashtag.objects.bulk_create( list(hashtag_bulk.values()) ,ignore_conflicts=True)
            Status.hashtags.through.objects.bulk_create( list(hashtag_bulk_through.values()) ,ignore_conflicts=True)

            UserMention.objects.bulk_create( list(userMention_bulk.values()) ,ignore_conflicts=True)
            Status.user_mentions.through.objects.bulk_create( list(userMention_bulk_through.values()) ,ignore_conflicts=True)

            User.urls.through.objects.bulk_create( list(url_bulk_through.values()) ,ignore_conflicts=True)
            User.descriptionUrl.through.objects.bulk_create( list(urlDescription_bulk_through.values()) ,ignore_conflicts=True)
            Status.urls.through.objects.bulk_create( list(urlStatus_bulk_through.values()) ,ignore_conflicts=True)
            Photo.objects.bulk_create( list(photos_bulk.values()),ignore_conflicts=True )
            Status.photos.through.objects.bulk_create(list(photoStatus_bulk.values()) ,ignore_conflicts=True)
            Video.objects.bulk_create( list(videos_bulk.values()),ignore_conflicts=True )
            Status.videos.through.objects.bulk_create(list(videosStatus_bulk.values()) ,ignore_conflicts=True)
            Gif.objects.bulk_create( list(gifs_bulk.values()),ignore_conflicts=True )
            Status.gifs.through.objects.bulk_create(list(gifsStatus_bulk.values()) ,ignore_conflicts=True)

            del users_bulk
            del status_bulk 
            del url_bulk
            del url_bulk_through 
            del urlDescription_bulk_through
            del hashtag_bulk
            del hashtag_bulk_through 
            del userMention_bulk
            del userMention_bulk_through
            del urlStatus_bulk_through
            del photos_bulk
            del photoStatus_bulk
            del videos_bulk
            del videosStatus_bulk
            del gifs_bulk
            del gifsStatus_bulk

            gc.collect()

            users_bulk = {}
            status_bulk = {}
            url_bulk = {}
            url_bulk_through = {}
            urlDescription_bulk_through = {}
            hashtag_bulk = {}
            hashtag_bulk_through = {}
            userMention_bulk = {}
            userMention_bulk_through = {}
            urlStatus_bulk_through = {}
            photos_bulk = {}
            photoStatus_bulk = {}
            videos_bulk = {}
            videosStatus_bulk = {}
            gifs_bulk = {}
            gifsStatus_bulk = {}




            print('wrote')

