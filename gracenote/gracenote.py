import pygn
import numpy as np
import codecs
import pickle



#Register pygn with client id. This is in a separate file to be used once per end user because
#each call to pygn.register goes towards a quota. We will need to run this for each user
#and store their UserID in our database. Then, we can query each song individually and store
#it's metadata in our database.

def register():

    gracenoteClientID = "58624-530E5E2D845DB16CB7D3A258CCCD5E07"
    gracenoteUserID = pygn.register(gracenoteClientID)

    return gracenoteUserID


gracenoteClientID = "58624-530E5E2D845DB16CB7D3A258CCCD5E07"
sampleUserID = "27396709641709153-2C0CF7D92465CE0CC6B7DC560EFCE44E"

def gracenoteSearch(user, album, artist, song):
    return pygn.search(clientID=gracenoteClientID, userID = user, artist=artist, album=album, track=song)


#print gracenoteSearch(sampleUserID, "", "The Beatles","Yellow")

musicFile = open("davidMusic.csv","r")

text = musicFile.readlines()[0]


songs = text.split("\r")

output = open("davidmusic.data","w")

#changID = "280442714066850429-1EBFB89D49DA659CB12786DFCE86883D"
#output.write("gracenoteID:" + changID + "\n")

userID = register()
musicData = {'userGNID':userID, 'data':[]}
print userID

ID = 0

for s in songs:
    sarray = s.split(",")
    if len(sarray) > 2:
        ID += 1
        artist = sarray[2]
        album = sarray[1]
        track = sarray[0]
        song = {'artist':artist,'album':album,'track':track}
        try:
            song['gnresult'] = gracenoteSearch(userID,album,artist,track)
            musicData['data'] += [song]
            print track
        except:
            print str(sarray) + "Decoding Error"
    else:
        print sarray

pickle.dump(musicData, output)
