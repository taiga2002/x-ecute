import tweepy
from datetime import datetime, timedelta
import xai_sdk
import asyncio

import re
from datetime import date
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Authentication credentials for Twitter API v2
bearer_token = "AAAAAAAAAAAAAAAAAAAAABmdtQEAAAAAzf5cxQJxz4tyAVx84vUCqL1v3Eo%3DMLmVpec8eUw6o67mABkfIjNCCR1GKUDL2BqZgctt0ymmxt0mfC"
client = tweepy.Client(bearer_token)

client_user = tweepy.Client(
    consumer_key="BoCHitvCkV87RESI4zUdXd8rH",
    consumer_secret="qA2huEattWw5jN3q38gHeYEbhtXDWFSxzGLzhgcFoXeau4dmX8",
    access_token="2686492698-HvkV6wwEta0Lb2HarYuWJCJ25vBq9VKzLAaNjGE",
    access_token_secret="ZZKTf15cCK9XQ9VWNeuSCmfg9X5IeuvhTCdW1lSDRKCsZ"
)

# Reader info

def get_user_info():
    # Fetch the authenticated user's username, name, and profile image URL in one go
    user_response = client_user.get_me(user_fields=['username', 'name', 'profile_image_url', 'public_metrics', 'verified', 'location'])
    if user_response.data:
        print("Name:", user_response.data.name)
        print("Username:", user_response.data.username)
        print("Profile Page URL:", user_response.data.profile_image_url)  # This is the user's profile image URL, not the page URL
        user_info = {
            "username": user_response.data.username,
            "displayName": user_response.data.name,
            "profilePicture": user_response.data.profile_image_url,
            "location": user_response.data.location,
            "verified": user_response.data.verified,
            "public_metrics": user_response.data.public_metrics
        }
        return user_info
    else:
        print("No data found for the authenticated user.")
        return None

user_info = get_user_info()

"""
CODE FOR LEXER
"""

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
        return func
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

def lex(code_segment, public_metrics):
    reserved = {
        "date_time": {
            "now": dateHelper()
        },
        "reader": {
            "location": user_info['location'],
            "verified": user_info['verified'],
            "friends_count": user_info['public_metrics']['following_count'],
            "followers_count": user_info['public_metrics']['followers_count']
        },
        "post": {
            "likes": public_metrics['like_count'],
            "reposts": public_metrics['retweet_count'],
            "views": public_metrics['impression_count'],
            "bookmarks": public_metrics['bookmark_count']
        }
    }
    split = splitter(code_segment, 2, reserved)
    split = flatten_list(split)
    print(split)
    return split

"""
CODE FOR CODE_GEN
"""

def gen(lst):
    animations = {
        "rocket": 0,
        "heart": 1
    }
    output = {
        "reword": "",
        "display": True,
        "animation": -1
    }
    for func in lst:
        split = func.split('.')
        if split[0] == "reword" and output["reword"] == "":
            output["reword"] = split[1]
        if split[0] == "animate" and output["animation"] == -1:
            output["animation"] = animations[split[1]]
        if split[0] == "display":
            output["display"] = False
    return output

"""
CODE FOR BACKEND APP
"""

def get_tweets(user_id):
    # Get tweets from Twitter API v2
    tweets = client.search_recent_tweets(query=f"from:{user_id}", max_results=10)
    
    # Format tweets into the desired format
    formatted_tweets = []
    for tweet in tweets.data:
        response = client.get_tweet(tweet.id, 
                            tweet_fields=['public_metrics'], 
                            expansions=['author_id'], 
                            user_fields=['username', 'name', 'profile_image_url', 'verified'])
        print(response)

        public_metrics = response.data.public_metrics

        # Map users by their IDs
        if response.includes and 'users' in response.includes and response.data:
            author = response.includes['users'][0]
            print(author)
        else:
            print("No user or tweet data available.")
            return []
        
        tweet_text = tweet.text
        code_text = ""
        if len(parsed := tweet_text.split(",.,\n")) > 1:
            tweet_text = parsed[0]
            code_text = parsed[1]

        lexical_analysis = lex(code_text, public_metrics)
        print(lexical_analysis)
        code_gen = gen(lexical_analysis)
        print(code_gen)

        #tweet_text = reword_text(code_gen["reword"], tweet_text) if code_gen["reword"] != "" else tweet_text

        formatted_tweet = {
            "bodyText": tweet_text,
            "display": True,
            "likeCount": public_metrics['like_count'],
            "retweetCount": public_metrics['retweet_count'],
            "replyCount": public_metrics['reply_count'],
            "shareCount": 0,
            "username": author.username,
            "displayName": author.name,
            "profilePicture": author.profile_image_url,
            "verified": author.verified,
            "rocket_launch": code_gen['animation']==0,
            "valentine": code_gen['animation']==1,
            "display": code_gen['display']
        }
        formatted_tweets.append(formatted_tweet)
    print(formatted_tweets)
    return formatted_tweets


def get_tweets_count(user_id, keyword, duration_days):
    
    # Calculate the start date based on the duration
    start_date = datetime.utcnow() - timedelta(days=duration_days)

    # Format the start date for the Twitter API query
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    print(start_date_str)
    # Construct the query string
    query = f"from:{user_id} {keyword}"

    # Get tweets matching the query from Twitter API v2
    tweets = client.search_all_tweets(query=query, start_time=start_date_str)

    # Return the number of tweets
    return len(tweets.data)


# Set Env as export XAI_API_KEY=Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ
def reword_text(user_prompt, text_content):
    client = xai_sdk.Client()
    conversation = client.grok.create_conversation()

    # Add the user prompt and the text content to the conversation
    response_coroutine = conversation.add_response(f"{user_prompt}\n\n{text_content}")
    response_token_stream, _ = response_coroutine

    # Iterate over the token stream to get the complete response
    response_text = ""
    for token in response_token_stream:
        response_text += token

    print(response_text)

# # Example usage:
# user_id = "TaigaKitao2002"
# keyword = "Hey"
# duration_days = 7

# tweets_count = get_tweets_count(user_id, keyword, duration_days)
# print("Number of tweets:", tweets_count)

# # Run the function
# user_prompt = "How can I reword this text for users more finance beginner friendly?"
# text_content = """Applied economists frequently use equilibrium displacement models (EDMs), also termed linear elasticity models, for policy analyses because they can be used to estimate changes in prices and quantities that result from exogenous economic or policy shocks. These models are also widely used to estimate changes in producer and consumer surplus caused by exogenous economic shocks and to quantify the short- and long-term impacts of a variety of economic and regulatory actions across multiple markets. For the first time, a textbook that contains all of the theory and applications of EDMs along with a set of spreadsheet files is available in one place."""


# asyncio.run(reword_text(user_prompt, text_content))

@app.route('/tweets', methods=['GET'])
def get_user_tweets():
    global user_info
    user_info = get_user_info()
    user_id = request.args.get('user_id')
    if user_id:
        tweets = get_tweets(user_id)
        print(tweets)
        return jsonify(tweets)
    else:
        return jsonify({"error": "Missing user_id parameter"}), 400
    
@app.route('/user', methods=['GET'])
def get_user():
    global user_info
    user_info = get_user_info()
    print(user_info)
    return jsonify(user_info)

if __name__ == '__main__':
    app.run(debug=True)
    # get_tweets("TaigaKitao2002")
