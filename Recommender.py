import numpy as np
import matplotlib 
import pandas as pd
import random as r
import collections
class Recommender:

    # Recommender constructor
    def __init__(self, userID):
        self.userID = userID
        # self.FLAG = True
        # self.songs = songs
        self.info = pd.read_csv(".\\databases\\song_info.csv")
        self.clusters = pd.read_csv(".\\databases\\cluster.csv")
        self.FavArtist = []
        self.history = pd.read_csv("history.csv")
        self.listeningHistorydf = pd.read_csv("listeningHistory.csv")
        self.listeningHistory = list(self.listeningHistorydf[self.listeningHistorydf.userID == userID].songList)
        self.recommendedSongs = list(self.history[self.history.userID == userID].songList)
        self.recommendedSongsbyArtist = []
    # get the index of a song from dataset
    def getIndex(self, s):
        try:
            INDEX = list(self.info.song_name).index(s)
            return INDEX
        except:
            return -1
    # returns the songs chosen by user
    '''
    def getMySongs(self):
        return self.songs
    '''
    
    # returns all the song info in the dataset
    def getAllSongInfo(self):
        return self.info
    # returns all the song cluster info 
    def getAllSongCluster(self):
        return self.clusters

    # Get recommended songs list
    def getRecommendedSongsByCluster(self):
        return self.recommendedSongs
    
    def getRecommendedSongsByArtist(self):
        return self.recommendedSongsbyArtist
        
    def listenToSong(self, song):
        # for
        self.listeningHistory.append(song)
        self.addToListeningHistory([song])
        
    '''
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
    '''
    # get N most popular songs in dataset wrt to artist
    def getNmostPopularSongsbyArtist(self, artist, N = 4):
        allsongByArtist = self.info[self.info.artist_name == artist]
        _songList = list(allsongByArtist.song_name)
        # allsongCluster = self.clusters[ self.clusters.name == _songList]
        popularity = []

        for s in _songList:
            popularity = list(self.clusters[ self.clusters.name == s].popularity)[0]
        # print(popularity)
        data = {'songList' : _songList, 'popularity' : popularity}
        _df = pd.DataFrame(data)
        _df = _df.sort_values(by = ['popularity'], ascending = False)
        
        #L =  return list(_df.head(N*4).songList)
        L = list(_df.head(N*4).songList)
        popularSong = []
        for s in L:
            i = r.randint(0,100)
            if i% 4 == 0:
                popularSong.append(s)
        return popularSong
    
    # get N most popular songs in a dataset wrt to a cluster
    def getNmostPopularSongs(self, cluster = -1, N = 4):
        
        # if cluster is -1, return 4 most popular songs in the whole dataset
        if cluster == -1:
            allsongCluster = self.getAllSongCluster()
            _df = allsongCluster.sort_values(by = ['popularity'], ascending = False)
            # return list(_df.head(N).name)

        # else return 4 most popular songs in that cluster
        else:
            allsongByCluster = self.clusters[self.clusters.cluster == cluster]
            _df = allsongByCluster.sort_values(by = ['popularity'], ascending = False)
            # return list(_df.head(N).name)
        L = list(_df.head(N*4).name)
        popularSong = []
        for s in L:
            i = r.randint(0,100)
            if i% 4 == 0:
                popularSong.append(s)
        return popularSong

    
    def getClusterOfaSong(self, song):
        return list(self.clusters[self.clusters['name'] == song]['cluster'])[0]
    def getArtistOfaSong(self, song):
        return list(self.info[self.info['song_name'] == song]['artist_name'])[0]
    
    #Recommend random popular song
    
    
    
    def recommendPopularSong(self):
        L = self.getNmostPopularSongs(N = 20)
        popularSong = []
        for s in L:
            i = r.randint(0,100)
            if i% 4 == 0:
                popularSong.append(s)
        return popularSong
    
    def addToListeningHistory(self, song):
        uID = []
        songList = []
        for s in song:
            uID.append(self.userID)
            songList.append(s)

        try:
            df = pd.read_csv("listeningHistory.csv")
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
            df.drop_duplicates(inplace = True)
            df.to_csv("listeningHistory.csv")
        return df
        
        
    def addToHistory(self, song):
        uID = []
        songList = []
        for s in song:
            uID.append(self.userID)
            songList.append(s)

        try:
            df = pd.read_csv("history.csv")
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
            df.drop_duplicates(inplace = True)
            df.to_csv("history.csv")
        return df
    
    def addToHistory_Favartist(self, mostPopArtist):
        uID = []
        # songList = []
        artistList = []
        for s in mostPopArtist:
            uID.append(self.userID)
            artistList.append(s)

        try:
            df = pd.read_csv("favartist.csv")
            _userID = list(df.userID)
            _userID.extend(uID)
            _artistList = list(df.artistList)
            _artistList.extend(artistList)
            data = {'userID' : _userID, 'artistList' : _artistList}
        except:
            print("no file exists")
            data = {'userID' : uID, 'artistList' : artistList}
        finally:
            df = pd.DataFrame(data)
            df.drop_duplicates(inplace = True)
            df.to_csv("favartist.csv")
        return df

    
    def getFromDB(self):
        df = pd.read_csv("history.csv")
        return df
    
    
    
    # recommender machine
    def recommend(self):
        
        # self.recommendedSongs = list(self.history[ self.history.userID == self.userID ].songList)
        if self.recommendedSongs == []:
            self.recommendedSongs.extend(self.recommendPopularSong())
        elif len(self.listeningHistory) < 4:
            # CREATE THE RECOMMENDER SYSTEM FOR RETURNING CUSTOMERS WITH NO LISTENING HISTORY
                # Get his recommendation history, 
                
                # get the clusters and artists of his history-songs
                L = self.recommendedSongs
                songCluster = []
                # songArtist = []
                for s in L:
                    songCluster.append(self.getClusterOfaSong(s))
                    # songArtist.append(self.getArtistOfaSong(s))
                
                # Choose 3 most popular cluster and 2 most popular artist
                _cluster = collections.Counter(songCluster).most_common(3)
                # _artist = collections.Counter(songArtist).most_common(2)
                mostPopCluster = []
                # mostPopArtist = []
                for d in _cluster:
                    mostPopCluster.append(d[0])
                '''
                for d in _artist:
                    mostPopArtist.append(d[0])
                
                self.FavArtist.extend(mostPopArtist)
                self.FavArtist = list(set(self.FavArtist))
                self.addToHistory_Favartist(mostPopArtist)
                '''
                # choose 4 most popular songs from 3 most popular clusters
                for c in mostPopCluster:
                    self.recommendedSongs.extend(self.getNmostPopularSongs(N = 3, cluster = c))
                # choose 4 most popular songs from 2 most popular artists
                '''
                for a in mostPopArtist:
                    SONGS = self.getNmostPopularSongsbyArtist(artist = a, N = 2)
                    self.recommendedSongsbyArtist.extend(SONGS)
                    self.recommendedSongs.extend(SONGS)
                '''
        else:
            # RECOMMENDATION FOR THOSE WHO HAVE LISTENING HISTORY
                L = self.listeningHistory
                songCluster = []
                songArtist = []
                for s in L:
                    songCluster.append(self.getClusterOfaSong(s))
                    songArtist.append(self.getArtistOfaSong(s))
                
                # Choose 3 most popular cluster and 2 most popular artist
                _cluster = collections.Counter(songCluster).most_common(3)
                _artist = collections.Counter(songArtist).most_common(3)
                mostPopCluster = []
                mostPopArtist = []
                for d in _cluster:
                    mostPopCluster.append(d[0])
                
                for d in _artist:
                    mostPopArtist.append(d[0])
                
                self.FavArtist.extend(mostPopArtist)
                self.FavArtist = list(set(self.FavArtist))
                self.addToHistory_Favartist(mostPopArtist)
                
                # choose 4 most popular songs from 3 most popular clusters
                for c in mostPopCluster:
                    self.recommendedSongs.extend(self.getNmostPopularSongs(N = 3, cluster = c))
                # choose 4 most popular songs from 2 most popular artists
                for a in mostPopArtist:
                    SONGS = self.getNmostPopularSongsbyArtist(artist = a, N = 2)
                    self.recommendedSongsbyArtist.extend(SONGS)
                    self.recommendedSongs.extend(SONGS)
                    
                    
        self.recommendedSongs = list(set(self.recommendedSongs))
        
        self.addToHistory(self.recommendedSongs)
        
    