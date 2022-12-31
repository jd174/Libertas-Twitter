from Modules.Logging.Logger import Logger
from Modules.Auth.FrontEndAuth import FrontEndAuth
from Modules.GetTweetLikes import GetLikers
 

def main():
    Logger.info("Starting Application...")
    LikeMachine=GetLikers()
    Likes=LikeMachine.GetLikes(Tweet=1608939190548598784)
    ParsedLikes=LikeMachine.parser(Likes)
    ParsedLikes.to_csv("Output.csv")
#main()