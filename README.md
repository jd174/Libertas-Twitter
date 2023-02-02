# Libertas Twitter
Gather info on tweets via the frontend API. No $150 monthly subscription required :)

When fed a Tweet ID the following values are returned for the users who liked the tweet:
          name	screen_name	id	description	location	statuses_count	verified	listed_count	created_at	favourites_count	followers_count	friends_count	            protected	  default_profile	default_profile_image	url

This information is returned as a CSV.


More features are soon to come with the announcement that twitter's backend API is being put behind a paywall. Feel free to fork ad collaborate on this.
  
  Features coming soon:
    ~ Like and send tweets
    ~ Edit profile


The rate limit on the front end API is 500 queries per 15min and around 90 users can be gathered per query. (Actually better than the old backend API)


Make sure to configure the ExampleConfig.txt file in this directory and then rename it as the comment in the file suggests. 
More documentation soon to come if this gets traction.
