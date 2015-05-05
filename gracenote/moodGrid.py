import pickle
import random
from decimal import Decimal
import math
import matplotlib.pyplot as plt
import numpy as np

moodCoords = {'Pastoral / Serene':[0,0], 'Delicate / Tranquil':[0,1], 'Hopeful / Breezy':[0,2], 'Cheerful / Playful':[0,3], 'Carefree Pop':[0,4], 'Party / Fun':[0,5], 'Showy / Rousing':[0,6], 'Lusty / Jaunty':[0,7], 'Loud Celebratory':[0,8], 'Euphoric Energy':[0,9],
'Reverent / Healing':[1,0], 'Quiet / Introspective':[1,1], 'Friendly':[1,2], 'Charming / Easygoing':[1,3], 'Soulful / Easygoing':[1,4], 'Happy / Soulful':[1,5], 'Playful / Swingin':[1,6], 'Exuberant / Festive':[1,7], 'Upbeat Pop Groove':[1,8], 'Happy Excitement':[1,9],
'Refined / Mannered':[2,0], 'Awakening / Stately':[2,1], 'Sweet / Sincere':[2,2], 'Heartfelt Passion':[2,3], 'Strong / Stable':[2,4], 'Powerful / Heroic':[2,5], 'Invigorating / Joyous':[2,6], 'Jubilant / Soulful':[2,7], 'Ramshackle / Rollicking':[2,8], 'Wild / Rowdy':[2,9],
'Romantic / Lyrical':[3,0], 'Light Groovy':[3,1], 'Dramatic / Romantic':[3,2], 'Lush / Romantic':[3,3], 'Dramatic Emotion':[3,4], 'Idealistic / Stirring':[3,5], 'Focused Sparkling':[3,6], 'Triumphant / Rousing':[3,7], 'Confident / Tough':[3,8], 'Driving Dark Groove':[3,9],
'Tender / Sincere':[4,0], 'Gentle Bittersweet':[4,1], 'Suave / Sultry':[4,2], 'Dark Playful':[4,3], 'Soft Soulful':[4,4], 'Sensual Groove':[4,5], 'Dark Sparkling Lyrical':[4,6], 'Fiery Groove':[4,7], 'Arousing Groove':[4,8], 'Heavy Beat':[4,9],
'Lyrical Sentimental':[5,0], 'Cool Melancholy':[5,1], 'Intimate Bittersweet':[5,2], 'Smoky / Romantic':[5,3], 'Dreamy Pulse':[5,4], 'Intimate Passionate':[5,5], 'Rhythm Energetic':[5,6], 'Abstract Groove':[5,7], 'Edgy / Sexy':[5,8], 'Abstract Beat':[5,9],
'Mysterious / Dreamy':[6,0], 'Light Melancholy':[6,1], 'Casual Groove':[6,2], 'Wary / Defiant':[6,3], 'Bittersweet Pop':[6,4], 'Energetic Yearning':[6,5], 'Dark Pop':[6,6], 'Dark Pop Intensity':[6,7], 'Heavy Brooding':[6,8], 'Hard Positive Excitement':[6,9],
'Wistful / Forlorn':[7,0], 'Sad / Soulful':[7,1], 'Cool Confidence':[7,2], 'Dark Groovy':[7,3], 'Sensitive / Exploring':[7,4], 'Energetic Dreamy':[7,5], 'Dark Urgent':[7,6], 'Energetic Anxious':[7,7], 'Attitude / Defiant':[7,8], 'Hard Dark Excitement':[7,9],
'Solemn / Spiritual':[8,0], 'Enigmatic / Mysterious':[8,1], 'Sober / Determined':[8,2], 'Strumming Yearning':[8,3], 'Melodramatic':[8,4], 'Hypnotic Rhythm':[8,5], 'Evocative / Intriguing':[8,6], 'Energetic Melancholy':[8,7], 'Dark Hard Beat':[8,8], 'Heavy Triumphant':[8,9],
'Dark Cosmic':[9,0], 'Creepy / Ominous':[9,1], 'Depressed / Lonely':[9,2], 'Gritty / Soulful':[9,3], 'Serious / Cerebral':[9,4], 'Thrilling':[9,5], 'Dreamy Brooding':[9,6], 'Alienated / Brooding':[9,7], 'Chaotic / Intense':[9,8], 'Aggressive Power':[9,9]}


musicData = pickle.load(open("davidmusic.data",'r'))

songMoods = []
songScores = []

#x = [i%10 for i in range(100)]
#y = []
#for i in range(10):
#    y += [i]*10
#num = np.zeros(100)
#N = 0

for entry in musicData['data']:
    try:
        moodLevel2 = entry['gnresult']['mood']['2']['TEXT']
        coords = moodCoords[moodLevel2]
        songMoods += [coords]
        num[coords[0] + 10*coords[1]] += 1
        N += 1
        songScores += [[str(entry['album']) + ' - ' + str(entry['artist']) + ' - ' + str(entry['track']), .5]]
    except:
        print "NO MOOD DATA: ", entry['album'], entry['artist'], entry['track']

    try:
        tempolevel2 = int(entry['gnresult']['tempo']['3']['TEXT'][0:2])
        print tempolevel2
    except:
        print "NO TEMPO DATA: ", entry['album'], entry['artist'], entry['track']

#s = np.zeros(100)
#for i in range(100):
#    s[i] = np.pi*num[i]**2
#plt.scatter(x, y, s=s)
#plt.show()


scores = []
for i in range(10):
    scores += [[.5]*10]

def printScores():
    print ''
    for row in scores:
        for val in row:
            print Decimal(val).quantize(Decimal('.001')),
        print ''

pleasentnessWeight = 1
energyWeight = 1

timeWeight = .5


def updateMoodScores(x, y, score):
    tot = 0;
    for i in range(len(scores)):
        for j in range(len(scores[i])):
            d = energyWeight*(x-i)**2 + pleasentnessWeight*(y-j)**2
            w = timeWeight*math.e**(-d)
            scores[i][j] = (1 - w)*scores[i][j] + w*score
            tot += scores[i][j]
    avg = tot/(len(scores)*len(scores[0]))
    for i in range(len(songScores)):
        songScores[i][1] = scores[songMoods[i][0]][songMoods[i][1]]

printScores()
updateMoodScores(3,3,.75)
printScores()
updateMoodScores(1,1,.25)
printScores()

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

#print songScores

#print weighted_choice(songScores)
#print weighted_choice(songScores)

