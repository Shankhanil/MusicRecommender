import numpy as np
import matplotlib 
import pandas as pd
import random as r

class Recommender:

    # Recommender constructor
    def __init__(self, userID, songs = []):
        self.userID = userID
        self.FLAG = True
        self.songs = songs
        self.info = pd.read_csv(".\\databases\\song_info.csv")
        self.clusters = pd.read_csv(".\\databases\\cluster.csv")
        self.recommendedSongs = []
        self.history = pd.read_csv("history.csv")
        
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
    
    # returns all the song info in the dataset
    def getAllSongInfo(self):
        return self.info
    # returns all the song cluster info 
    def getAllSongCluster(self):
        return self.clusters

    # Get recommended songs list
    def getRecommendedSongs(self):
        return self.recommendedSongs
    
    # get the <song name, artist, cluster> of the songs chosen by user
    def getAllSongsDataframe(self):
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
    def getNmostPopularSongs(self, cluster = -1, N = 4):
        
        # if cluster is -1, return 4 most popular songs in the whole dataset
        if cluster == -1:
            allsongCluster = self.getAllSongCluster()
            _df = allsongCluster.sort_values(by = ['popularity'], ascending = False)
            return list(_df.head(N).name)

        # else return 4 most popular songs in that cluster
        else:
            return ['cluster-ful']

    def getClusterOfaSong(self, song):
        return self.clusters[self.clusters['name'] == song]['cluster']
    # recommender machine
    def recommend(self):
        L = list(self.history[ self.history.userID == self.userID ].songList)
        if L ==  []:
            self.recommendedSongs.extend(self.getNmostPopularSongs())
        else:
            # CREATE THE RECOMMENDER SYSTEM FOR RETURNING CUSTOMERS
                # Get his history, 
                # get the clusters of his history-songs
                Sclusters = []
                for s in L:
                    Sclusters.append(self.getClusterOfaSong(s))
                # choose 4 most popular songs from 3 most popular clusters
                
                # choose 4 most popular songs from 2 most popular artists
                
                self.recommendedSongs.extend(['abc', 'def'])
        self.recommendedSongs = list(set(self.recommendedSongs))
        self.addToDB(self.recommendedSongs)
            # print(df)
    
    def addToDB(self, song):
        uID = []
        songList = []
        for s in song:
            uID.append(self.userID)
            songList.append(s)
        
        try:
            df = pd.read_csv("history.csv")
            # df = pd.concat([df, _df], ignore_index = True)
            _userID = list(df.userID)
            _userID.extend(uID)
            _songList = list(df.songList)
            _songList.extend(songList)
            data = {'userID' : _userID, 'songList' : _songList}
        except:
            print("no file exists")
            data = {'userID' : uID, 'songList' : songList}
        finally:
            df = pd.DataFrame(data)
            df.to_csv("history.csv")
        return df
    
    
    def getFromDB(self):
        df = pd.read_csv("history.csv")
        return df