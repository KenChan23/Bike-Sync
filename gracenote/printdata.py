import pickle
import codecs

musicData = pickle.load(open("davidmusic.data",'r'))
fields = ['track_title','genre','tempo','mood','track_number','artist_era','artist_origin','artist_type']

f = open("formattedDavid2.txt","w")

for entry in musicData['data']:
    f.write( entry['artist'] +' - ' +entry['album'] +' - ' +entry['track'] + '\n')
    gnresult = entry['gnresult']
    for k in fields:
        if k in gnresult.keys():
            p = gnresult[k]
            if p is not "":
                f.write( '\t' + str(k) +':\n')
                try:
                    for k2 in p.keys():
                        f.write( "\t\t"+unicode(p[k2]) + '\n')
                except:
                    s = unicode(p)
                    f.write( "\t\t" + s.encode('utf16') + '\n')
    f.write( "\n\n")
