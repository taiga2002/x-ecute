import tweepy
from datetime import datetime, timedelta
import xai_sdk
import asyncio
from flask import Flask, jsonify, request
# Authentication credentials for Twitter API v2
bearer_token = "AAAAAAAAAAAAAAAAAAAAABmdtQEAAAAAzf5cxQJxz4tyAVx84vUCqL1v3Eo%3DMLmVpec8eUw6o67mABkfIjNCCR1GKUDL2BqZgctt0ymmxt0mfC"
app = Flask(__name__)
# Instantiate the Client with bearer token authentication
client = tweepy.Client(bearer_token)

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
        
        public_metrics = response.data.public_metrics
        users = {user.id: user for user in response.includes['users']}
        
        # Map users by their IDs
        if response.includes['users'] and response.data:
            first_user = response.includes['users'][0]
            first_tweet = response.data
        else:
            print("No user or tweet data available.")
            return []
        # print(users)
        # author = users[tweet.author_id]
        # likes = response.data.public_metrics['like_count']
        # print(response.data.public_metrics)
        # print(f'The tweet has {likes} likes.')
        formatted_tweet = {
            "bodyText": tweet.text,
            "javascript": "",
            "display": True,
            "likeCount": public_metrics['like_count'],
            "retweetCount": public_metrics['retweet_count'],
            "replyCount": public_metrics['reply_count'],
            "shareCount": 0,
            "username": first_user.username,
            "displayName": first_user.name,
            "profilePicture": "fake_URL",
            "verified": False,
            "animation": "",
            "display": True
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
async def reword_text(user_prompt, text_content):
    client = xai_sdk.Client()
    conversation = client.grok.create_conversation()

    # Add the user prompt and the text content to the conversation
    response_coroutine = conversation.add_response(f"{user_prompt}\n\n{text_content}")
    response_token_stream, _ = response_coroutine

    # Iterate over the token stream to get the complete response
    response_text = ""
    async for token in response_token_stream:
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
    user_id = request.args.get('user_id')
    if user_id:
        tweets = get_tweets(user_id)
        return jsonify(tweets)
    else:
        return jsonify({"error": "Missing user_id parameter"}), 400

if __name__ == '__main__':
    app.run(debug=True)
    # get_tweets("TaigaKitao2002")
