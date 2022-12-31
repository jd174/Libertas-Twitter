import json 
import time 
import requests
import pandas as pd 
from concurrent.futures import ThreadPoolExecutor , as_completed
from datetime import date
from pathlib import Path
import logging
import sys
import os
from .Auth import FrontEndAuth as FEAuth

class GetLikers: 
    def __init__(self):
        self.reauth=False
        self.Cookies=self.Auth()
        self.THREAD_COUNT = 10
        self.FinalUserInfo=[]
    
    def Auth(self):
        AuthPath=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Auth/FrontEndCookies.json')
        if not os.path.exists(AuthPath) or self.reauth==True:
            FEAuth.FrontEndAuth()
        with open(AuthPath, 'r') as openfile:
            Cookies = json.load(openfile)
        return(Cookies)

    def is_valid(self, json, key): 
        if not isinstance(json, dict): 
            return None 
        if key in json.keys(): 
            return key 
        ans = None 
        for json_key in json.keys(): 
            r = self.is_valid(json[json_key], key) 
            if r is None: 
                continue 
            else: 
                ans = "{}.{}".format(json_key, r) 
        return ans 
 
    def get_abs_path(self, json, key): 
        path = self.is_valid(json, key) 
        return (path) 
 
    def find(self, element, json): 
        keys = element.split('.') 
        rv = json 
        for key in keys: 
            rv = rv[key] 
        return rv 
 
    def GetCursor(self, x, Cursor): 
        if Cursor == str(x['content']['value']): 
            return ("STOP") 
        else: 
            Cursor = str(x['content']['value']) 
            return (Cursor) 
    
    def parser(self,responseList):
        DesiredFields=[
        'name',
        'screen_name',
        'rest_id',
        'description',
        'location',
        'url',
        'statuses_count',
        'verified',
        'listed_count',
        'created_at',
        'verified',
        'lang',
        'status',
        'has_extended_profile',
        'favourites_count',
        'followers_count',
        'friends_count',
        'protected',
        'default_profile',
        'default_profile_image']
        AllUsers=[]
        for x in responseList:
            UserList = x['data']['favoriters_timeline']['timeline']['instructions'][0]['entries']
            for user in UserList:
                if user['content']['entryType'] != "TimelineTimelineCursor":
                    Userinfo = {}
                    for field in DesiredFields: 
                        path = self.get_abs_path(user, field)
                        if path != None: 
                            Userinfo[field] = self.find(path, user)
                if Userinfo != {}:
                    AllUsers.append(Userinfo)
        df=pd.DataFrame.from_records(AllUsers)
        df=df.drop_duplicates()
        df=df.rename(columns={"rest_id":"id"})
        return(df)

    def GetLikes(self, Tweet):
        logging.info("Gathering Likes for tweet: "+str(Tweet))
        try:
            Cursor = 0 
            AllResponses=[]
            remainingQueries=1
            ResetTime=1
            while Cursor != "STOP":
                if remainingQueries == 0:
                    logging.info("Rate Limit exceeded... Waiting to continue.")
                    print("Rate Limit exceeded... Waiting to continue.")
                    while int(time.time())<ResetTime:
                        time.sleep(1)
                cookies = { 
                    'personalization_id': self.Cookies['personalization_id'], 
                    'kdt': self.Cookies['kdt'], 
                    'auth_token': self.Cookies['auth_token'], 
                    'ct0': self.Cookies['ct0'],
                    'twid': self.Cookies['twid'],
                    'att': self.Cookies['att'],
                }
    
                headers = { 
                    'authority': 'twitter.com', 
                    'accept': '*/*', 
                    'accept-language': 'en-US,en;q=0.9', 
                    'authorization': self.Cookies['Bearer'], 
                    'content-type': 'application/json', 
                    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"', 
                    'sec-ch-ua-mobile': '?0', 
                    'sec-ch-ua-platform': '"Windows"', 
                    'sec-fetch-dest': 'empty', 
                    'sec-fetch-mode': 'cors', 
                    'sec-fetch-site': 'same-origin', 
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 
                    'x-csrf-token': self.Cookies['ct0'], 
                    'x-twitter-active-user': 'yes', 
                    'x-twitter-auth-type': 'OAuth2Session', 
                    'x-twitter-client-language': 'en', 
                } 
                params = { 
                    'variables': '{"tweetId":' + str(Tweet) + ',"count":400,"cursor":"' + str( 
                        Cursor) + '","includePromotedContent":true,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}', 
                    'features': '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"view_counts_public_visibility_enabled":false,"view_counts_everywhere_api_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_uc_gql_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":true}', 
                } 
    
                response = requests.get( 
                    'https://twitter.com/i/api/graphql/ZD3hAo97BbofWpy43e9uUw/Favoriters', 
                    params=params, 
                    cookies=cookies, 
                    headers=headers, 
                ) 
                remainingQueries=response.headers['x-rate-limit-remaining']
                ResetTime=response.headers['x-rate-limit-reset']
                UserList = response.json()['data']['favoriters_timeline']['timeline']['instructions'][0]['entries']
                for x in UserList: 
                    if str('cursor-bottom') in str(x['entryId']): 
                        Cursor = self.GetCursor(x, Cursor)
                AllResponses.append(response.json())
        except Exception as e:
            logging.info("There was an error gathering tweet likes on "+str(Tweet))
            logging.info(str(e))
            sys.exit()
        return(AllResponses) 
 

 