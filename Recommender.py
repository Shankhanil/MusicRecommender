import numpy as np
import matplotlib 
import pandas as pd
import random as r

class Recommender:
    def __init__(self, songs):
        self.songs = songs
        self.info = pd.read_csv(".\\databases\\song_info.csv")
    def getIndex(self, s):
        try:
            INDEX = list(self.info.song_name).index(s)
            return INDEX
        except:
            return -1

    def getDataframe(self):
        sname = []
        artist = []
        cluster = []
        
        for s in self.songs:
            #n = r.randint(0, 18836)
            INDEX = self.getIndex(s)
            if INDEX == -1:
                print ("Not found!")
                # pass
            else:
                sname.append(s)
                artist.append(self.info.iloc[INDEX].artist_name)
            #cluster.append(clusters[ clusters['name'] ==  song]['cluster'])
        data = {'song': sname, 'artist' : artist}
        df = pd.DataFrame(data)
        print(df)
        #df.to_csv("res.csv")
        #return df
