import numpy as np
import matplotlib 
import pandas as pd
import random as r

class Recommender:

    # Recommender constructor
    def __init__(self, songs = []):
        self.FLAG = True
        self.songs = songs
        self.info = pd.read_csv(".\\databases\\song_info.csv")
        self.clusters = pd.read_csv(".\\databases\\cluster.csv")
        self.recommendedSongs = []
        
        
        
    # get the index of a song from dataset
    def getIndex(self, s):
        try:
            INDEX = list(self.info.song_name).index(s)
            return INDEX
        except:
            return -1
    # returns the songs chosen by user
    def getMySongs(self):
        return self.songs
    
    # returns all the songs in the dataset
    def getAllSongInfo(self):
        return self.info
    def getAllSongCluster(self):
        return self.clusters

    # Get recommended songs list
    def getRecommendedSongs(self):
        return self.recommendedSongs
    
    # get the <song name, artist, cluster> of the songs chosen by user
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
                cluster.append(self.clusters[ clusters['name'] ==  song]['cluster'])

        data = {'song': sname, 'artist' : artist, 'cluster' : cluster}
        df = pd.DataFrame(data)
        # print(df)
        df.to_csv("res.csv")
        return df
    
    # get 4 most popular songs in a dataset wrt to a cluster
    def getmostPopularSongs(self, cluster = -1):
        
        # if cluster is -1, return 4 most popular songs in the whole dataset
        if cluster == -1:
            allsongCluster = self.getAllSongCluster()
            _df = allsongCluster.sort_values(by = ['popularity'], ascending = False)
            return list(_df.head(4).name)

        # else return 4 most popular songs in that cluster
        else:
            return ['cluster-ful']

    
    # recommender machine
    def recommend(self):
        if self.FLAG == True:
            self.recommendedSongs.extend(self.getmostPopularSongs())
            self.FLAG = False
