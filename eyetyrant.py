import config
import tweepy
import json
import sys
from hangpw  import Hangman
from guess_number import Guess_number


auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

class GameBot(tweepy.streaming.StreamListener):

    def __init__(self):
        self.current_games = {}
        self.game_number = 0

    def on_data(self, data):
        tweet = json.loads(data)
        retweeted = tweet.get('retweeted')

        print(tweet)        
        

        try:
            from_self = tweet.get('user',{}).get('id_str','') == config.OWNER_ID            
            if  "id" in tweet and retweeted is not None and not retweeted: # and not from_self:
                screenName = tweet.get('user',{}).get('screen_name')
                tweetId = tweet.get('id_str')                
                tweetText = tweet.get('text').replace("@"+config.OWNER+" ", "")
                tweet_reply_id = tweet.get('in_reply_to_status_id')
                new_game = None
                print(tweetText)

                if "play numbers" in tweetText.lower():                    
                    new_game = self.game_factory("numbers")
                elif "play hangpw" in tweetText.lower():
                    new_game = self.game_factory("hangman")
                    print(new_game.hidden_word)

                if new_game:
                    new_status = "@" + screenName + "\n" + new_game.play()
                    update = api.update_status(status=new_status, in_reply_to_status_id=tweetId)                    
                    self.current_games[update.id] = new_game
                    new_game = None
                elif tweet_reply_id in self.current_games:
                    new_status = "@" + screenName + "\n" + self.current_games[tweet_reply_id].move(tweetText)
                    update = api.update_status(status=new_status, in_reply_to_status_id=tweetId)
                    if not self.current_games[tweet_reply_id].game_over():
                        self.current_games[update.id] = self.current_games[tweet_reply_id]
                    del self.current_games[tweet_reply_id]


        except:
            e = sys.exc_info()[0]


    def game(self, text, reply_id):      
        if(reply_id not in self.current_games):
            self.current_games[reply_id] = Guess_number()
        else:
            self.current_games[reply_id].move()

        return "GAME ON!"

    def game_factory(self, game_name):
        game = None
        if game_name =="hangman":
            pw = []
            with open("top_1000_pw.txt", 'r') as f:
                pw = f.readlines()
            pw = [x.strip() for x in pw] 
            game = Hangman(pw)
        elif game_name == "numbers":
            game = Guess_number()
        return game



if __name__ == "__main__":
    bot = GameBot()
    stream = tweepy.Stream(auth, bot)
    stream.userstream(_with='user')
    


