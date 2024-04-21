import re
from datetime import date
import tweepy

client_user = tweepy.Client(
    consumer_key="KNpW9bkrWWCiUS62w1SJrerOb",
    consumer_secret="P0cew3ZDqPLDIHEds3kWi0G9ZPbznqA8DAlaz5YutzdKYun8mJ",
    access_token="3058762748-r3NY8ktxccNRrRlrJghhvnIibCMpgN6hN0g3GK2",
    access_token_secret="jyfUDwFpaR31YoXph3TYQz9W00xFTglHWb97034T71gF5"
)

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
        tweet = self.get_tweet()
        return tweet.public_metrics['like_count']

    def tweet_retweet(self):
        """Get the number of retweets."""
        tweet = self.get_tweet()
        return tweet.public_metrics['retweet_count']
    
    def tweet_views(self):
        """Get the number of views for a tweet."""
        tweet = self.get_tweet()
        return tweet.public_metrics['impression_count']
    
    def tweet_bookmarks(self):
        """Get the number of bookmarks for a tweet."""
        tweet = self.get_tweet()
        return tweet.public_metrics['bookmark_count']

class ReaderInfo:
    """Class to fetch information about the audience using Twitter API v2."""
    def __init__(self, client):
        self.client = client

    def get_user(self):
    # Fetch the authenticated user's username, name, and profile image URL in one go
        user_response = client_user.get_me(user_fields=['public_metrics', 'verified', 'location'])
        if user_response.data:
            user_info = {
                "public_metrics": user_response.data.public_metrics,
                "verified": user_response.data.verified,
                "location": user_response.data.location
            }
            return user_info
        else:
            print("No data found for the authenticated user.")
            return None

    def location(self):
        """Get the location of the user."""
        user = self.get_user()
        return user['location']

    def verified(self):
        """Check if the user is verified."""
        user = self.get_user()
        return user['verified']

    def friends_count(self):
        """Get the number of friends (followers) the user has."""
        user = self.get_user()
        return user['public_metrics']['following_count']

    def followers_count(self):
        """Get the number of followers."""
        user = self.get_user()
        return user['public_metrics']['followers_count']


def start(tweet_id):
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAABmdtQEAAAAAzf5cxQJxz4tyAVx84vUCqL1v3Eo%3DMLmVpec8eUw6o67mABkfIjNCCR1GKUDL2BqZgctt0ymmxt0mfC'
    client = authenticate(bearer_token)

    # Create instances of TweetInfo and ReaderInfo
    tweet_info = TweetInfo(client, tweet_id)
    reader_info = ReaderInfo(client)
    return tweet_info, reader_info

def splitter(text, num, reserved):
    # Split on '\n' only when not followed by ' '
    parts = re.split(r'\n(?!\s)', text)
    for i in range(len(parts)):
        if i > 0 and len(parts[i]) > 4 and ("else" == parts[i][0:4] or "elif" == parts[i][0:4]) and parts[i-1]:
            parts[i] = []
            continue
        adder = []
        # print([parts[i]])
        while '\n' in parts[i]:
            parts[i] = extracter(parts[i], str(num), reserved)
            if len(parts[i]) > 1:
                for j in range(len(parts[i])):
                    if j > 0 and len(parts[i][j]) > 4 and ("else" == parts[i][j][0:4] or "elif" == parts[i][j][0:4]) and adder[j-1]:
                        adder.insert(0, [])
                        continue
                    adder = adder + splitter(parts[i][j], num + 2, reserved)
        if adder:
            parts[i] = adder
            parts[i] = flatten_list(parts[i])
    # print(parts)
    return parts

def extracter(text, num, reserved):
    inner = re.split(r'\n(?=\s{'+ num + '}[^ ])', text)
    # print(inner)
    cont = evaluate(inner[0], reserved)
    if not cont:
        return []
    inner = inner[1:]
    for i in range(len(inner)):
        inner[i] = inner[i].strip()
    return inner

def evaluate(text, reserved):
    # print(text)
    andSplit = re.split(r'\s+(and|or)\s+', text)
    
    result = andSplit

    # print(result)
    output = False
    if len(result) > 1:
        for i in range(len(result)):
            if result[i] == 'and':
                return evaluate(result[i-1], reserved) and evaluate(result[i+1], reserved)
            if result[i] == 'or':
                if evaluate(result[i-1], reserved) or evaluate(result[i+1], reserved):
                    return True
            
    tok = re.split(r'\s+(==|>|>=|<|<=)\s+', text)
    if len(tok) == 1:
        return True
    left = tok[0]
    if "elif" in left:
        left = left[5:]
    if "if" in left:
        left = left[3:]
    left = reduce(left, reserved)
    right = tok[2]
    right = reduce(right, reserved)
    if tok[1] == "==":
        if left == right:
            return True
    if tok[1] == ">":
        if left > right:
            return True
    if tok[1] == ">=":
        if left >= right:
            return True
    if tok[1] == "<":
        if left < right:
            return True
    if tok[1] == "<=":
        if left <= right:
            return True
    if tok[1] == "!=":
        if left != right:
            return True
    return False

def reduce(text, reserved):
    if ' ' not in text and '.' in text:
        special = text.split('.')
        func = reserved[special[0]][special[1]]
        print(func())
        return func()
    if text[0] == '"':
        return text[1:len(text) - 1]
    if text == "True":
        return True
    if text == "False":
        return False
    output = ""
    tok = text.split(' ')
    for token in range(len(tok)):
        if tok[token] == '+':
            if output:
                output = str(int(output) + int(reduce(tok[token + 1], reserved)))
            else:
                output = str(int(reduce(tok[token - 1], reserved)) + int(reduce(tok[token + 1], reserved)))
        elif tok[token] == '-':
            if output:
                output = str(int(output) - int(reduce(tok[token + 1], reserved)))
            else:
                output = str(int(reduce(tok[token - 1], reserved)) - int(reduce(tok[token + 1], reserved)))
        elif tok[token] == '*':
            if output:
                output = str(int(output) * int(reduce(tok[token + 1], reserved)))
            else:
                output = str(int(int(reduce(tok[token - 1], reserved))) * int(reduce(tok[token + 1], reserved)))
        elif tok[token] == '//':
            if output:
                output = str(int(output) // int(reduce(tok[token + 1], reserved)))
            else:
                output = str(int(int(reduce(tok[token - 1], reserved))) // int(reduce(tok[token + 1], reserved)))
        elif tok[token] == '%':
            if output:
                output = str(int(output) % int(reduce(tok[token + 1], reserved)))
            else:
                output = str(int(int(reduce(tok[token - 1], reserved))) % int(reduce(tok[token + 1], reserved)))
    if not output:
        try:
            x = int(text)
            return x
        except:
            return text
    return int(output)

def flatten_list(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

def dateHelper():
    return str(date.today())


"""
if 5 + 3 == 12 - 4 and 4 == 14 % 5 or 5 == 3
  fn()
  if 3 * 6 == 54 // 3 and "abc" <= "abd"
    fn2()
    if False == True
      fn4()
    elif True == True and 4 == 4
      fn5()
    else
      fn6()
elif 4 == 4
  fn3()
"""
# output = ['fn()', 'fn2()', 'fn5()']

def lex(code_segment, tweet_id):
    tweet, reader = start(tweet_id)

    reserved = {
        "date_time": {
            "now": dateHelper
        },
        "reader": {
            "location": reader.location,
            "verified": reader.verified,
            "friends_count": reader.friends_count,
            "followers_count": reader.followers_count
        },
        "tweet": {
            "likes": tweet.tweet_likes,
            "retweets": tweet.tweet_retweet,
            "views": tweet.tweet_views,
            "bookmarks": tweet.tweet_bookmarks
        }
    }
    split = splitter(code_segment, 2, reserved)
    split = flatten_list(split)
    print(split)
    return split

if __name__ == "__main__":
    lex("if 5 + 3 == 12 - 4 and 4 == 14 % 5 or 5 == 3\n  fn()\n  if 3 * 6 == 54 // 3 and \"abc\" <= \"abd\"\n    fn2()\n    if False == True\n      fn4()\n    elif True == True and 4 == 4\n      fn5()\n    else\n      fn6()\nelif 4 == 4\n  fn3()", "1781866717238456650")
    lex("if date_time.now != \"2024-04-22\"\n  reword.Remove Swear Words", "1781866717238456650")
    lex('if date_time.now == "2024-02-14"\n  animate.heart\nelif tweet.likes % 2 == 0\n  reword.make this tweet into a poem\nelse\n  display.hide', "1782012917711503493")