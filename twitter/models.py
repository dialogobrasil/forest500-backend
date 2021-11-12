from django.db import models

class Hashtag(models.Model):
    text = models.TextField(primary_key=True)

class UserMention(models.Model):
    screen_name = models.TextField()
    name = models.TextField()
    id = models.TextField(primary_key=True)

    def __str__(self):
        return self.screen_name

class Url(models.Model):
    url = models.URLField(max_length=500,primary_key=True)
    expanded_url = models.URLField(blank=True,null=True,max_length=500)
    display_url = models.URLField(blank=True,null=True,max_length=500)

    def __str__(self):
        return self.url

class PinnedTweet(models.Model):
    id = models.TextField(primary_key=True)
    user = models.ForeignKey('User',on_delete=models.PROTECT)

class AdvertiserAccountServiceLevel(models.Model):
    advertiser_account_service_levels = models.TextField()
    user = models.ForeignKey('USer',on_delete=models.PROTECT)
    

class User(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    screen_name = models.TextField()
    location = models.TextField()
    description = models.TextField()
    urls = models.ManyToManyField(Url,related_name='urls')
    descriptionUrl = models.ManyToManyField(Url,related_name='description_url')
    protected = models.BooleanField()
    followers_count = models.BigIntegerField()
    fast_followers_count = models.BigIntegerField(blank=True,null=True)
    normal_followers_count = models.BigIntegerField(blank=True,null=True)
    friends_count = models.BigIntegerField()
    listed_count = models.BigIntegerField()
    created_at = models.DateTimeField()
    favourites_count = models.BigIntegerField()
    geo_enabled = models.BooleanField()
    verified = models.BooleanField()
    statuses_count = models.BigIntegerField()
    media_count = models.BigIntegerField(blank=True,null=True)
    lang = models.TextField(null=True)
    contributors_enabled = models.BooleanField()
    is_translator = models.BooleanField()
    is_translation_enabled = models.BooleanField()
    profile_background_color = models.TextField()
    profile_background_image_url = models.URLField(null=True)
    profile_background_image_url_https = models.URLField(null=True)
    profile_background_tile = models.BooleanField()
    profile_image_url = models.URLField(null=True)
    profile_image_url_https = models.URLField(null=True)
    profile_banner_url = models.URLField(null=True)
    profile_link_color = models.TextField()
    profile_sidebar_border_color = models.TextField()
    profile_sidebar_fill_color = models.TextField()
    profile_text_color = models.TextField()
    profile_use_background_image = models.BooleanField()
    has_custom_timelines = models.BooleanField(blank=True,null=True)
    advertiser_account_type = models.TextField(blank=True,null=True)
    analytics_type = models.TextField(blank=True,null=True)
    translator_type = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.screen_name

class Place(models.Model):
    bounding_box = models.TextField()
    country = models.TextField()
    country_code = models.TextField()
    full_name = models.TextField()
    id = models.TextField(primary_key=True)
    name = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.full_name
    
class Photo(models.Model):
    id = models.TextField(primary_key=True)
    media_url = models.URLField()
    media_url_https = models.URLField()
    url = models.ForeignKey(Url,on_delete=models.PROTECT)
    media_key = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.media_url

class Video(models.Model):
    id = models.TextField(primary_key=True)
    media_url = models.URLField()
    media_url_https = models.URLField()
    url = models.ForeignKey(Url,on_delete=models.PROTECT)
    media_key = models.TextField(blank=True,null=True)
    aspect_ratio_x = models.IntegerField()
    aspect_ratio_y = models.IntegerField()
    duration_millis = models.BigIntegerField()
    video_url = models.URLField()

    def __str__(self):
        return self.media_url

class Gif(models.Model):
    id = models.TextField(primary_key=True)
    media_url = models.URLField()
    media_url_https = models.URLField()
    url = models.ForeignKey(Url,on_delete=models.PROTECT)
    display_url = models.URLField()
    expanded_url = models.URLField()
    media_key = models.TextField(blank=True,null=True)
    aspect_ratio_x = models.IntegerField()
    aspect_ratio_y = models.IntegerField()
    gif_url = models.URLField()

    def __str__(self):
        return self.media_url

class Status(models.Model):
    created_at = models.DateTimeField()
    id = models.TextField(primary_key=True)
    content = models.TextField()
    display_text_range_start = models.IntegerField()
    display_text_range_end = models.IntegerField()
    hashtags = models.ManyToManyField(Hashtag)
    user_mentions = models.ManyToManyField(UserMention)
    urls = models.ManyToManyField(Url)
    source = models.TextField()
    in_reply_to_status_id = models.TextField(null=True)
    in_reply_to_user_id = models.TextField(null=True)
    in_reply_to_screen_name = models.TextField(null=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    place = models.ForeignKey(Place,on_delete=models.PROTECT,null=True, blank=True)
    is_quote_status = models.BooleanField()
    retweet_count = models.BigIntegerField()
    favorite_count = models.BigIntegerField()
    conversation_id = models.TextField(blank=True,null=True)
    possibly_sensitive = models.BooleanField(null=True,blank=True)
    possibly_sensitive_editable = models.BooleanField(null=True,blank=True)
    lang = models.TextField()
    retweet_status = models.ForeignKey('self',on_delete=models.PROTECT,related_name='retweet',blank=True,null=True)
    quoted_status = models.ForeignKey('self',on_delete=models.PROTECT,related_name='quoted',blank=True,null=True)
    photos = models.ManyToManyField(Photo,related_name='photos')
    videos = models.ManyToManyField(Video,related_name='videos')
    gifs = models.ManyToManyField(Gif,related_name='gifs')

    def __str__(self):
        return self.content
    
