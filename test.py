from Recommender import Recommender
import pandas as pd
if __name__ == "__main__":
    
    rc = Recommender()
    
    allsongInfo = rc.getAllSongInfo()
    rc.recommend()
    print(rc.getRecommendedSongs())
    