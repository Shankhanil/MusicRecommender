from Recommender import Recommender
import pandas as pd
if __name__ == "__main__":
    
    rc = Recommender(userID = 1)
    
    allsongInfo = rc.getAllSongInfo()
    rc.recommend()
    L = rc.getRecommendedSongs()
    rc.recommend()