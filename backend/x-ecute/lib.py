import tweepy

# Initialize and authenticate Tweepy API v2
def authenticate(bearer_token):
    client = tweepy.Client(bearer_token)
    return client

class TweetInfo:
    """Class to fetch information about tweets using Twitter API v2."""
    def __init__(self, client, tweet_id):
        self.client = client
        self.tweet_id = tweet_id

    def get_tweet(self):
        """Retrieve a specific tweet by ID with additional metrics."""
        tweet = self.client.get_tweet(self.tweet_id, tweet_fields=["public_metrics"])
        return tweet.data

    def tweet_likes(self):
        """Get the number of likes for a tweet."""
        tweet = self.get_tweet(self.tweet_id)
        return tweet.public_metrics['like_count']

    def tweet_retweet(self):
        """Get the number of retweets."""
        tweet = self.get_tweet(self.tweet_id)
        return tweet.public_metrics['retweet_count']

class ReaderInfo:
    """Class to fetch information about the audience using Twitter API v2."""
    def __init__(self, client, user_id):
        self.client = client
        self.user_id = user_id

    def get_user(self):
        """Retrieve user details."""
        user = self.client.get_user(self.user_id, user_fields=["public_metrics", "verified", "description", "location"])
        return user.data

    def location(self):
        """Get the location of the user."""
        user = self.get_user()
        return user.location

    def verified(self):
        """Check if the user is verified."""
        user = self.get_user()
        return user.verified

    def friends_count(self):
        """Get the number of friends (followers) the user has."""
        user = self.get_user()
        return user.public_metrics['following_count']

    def followers_count(self):
        """Get the number of followers."""
        user = self.get_user()
        return user.public_metrics['followers_count']