import sqlite3
from urllib.parse import urlparse
import numpy as np
import matplotlib.pyplot as plt

databaseFilename = 'places2.sqlite'
conn = sqlite3.connect(databaseFilename)
c = conn.cursor()

c.execute('SELECT * FROM moz_historyvisits')
historyvisits = c.fetchall()

c.execute('SELECT * FROM moz_places')
places = c.fetchall()

hostNames = {}

print(len(places))

for visit in historyvisits:
    #print('\nNow:')
    # place number of visit
    visitPlaceId = visit[2]
    if(visitPlaceId < 1):
        print('Less than 1!')
    #print('VisitPlaceId:' + str(visitPlaceId))
    # get url associated with that place, table is 1-indexed so we have to subtract 1
    c.execute('SELECT * FROM moz_places WHERE id = ' + str(visitPlaceId))
    place = c.fetchone()
    visitUrl = place[1]
    #print('Url: ' + str(visitUrl))
    # get only hostname of url using urllib
    visitHostname = urlparse(visitUrl).hostname
    #print('Hostname:' + str(visitUrl))
    if visitHostname in hostNames:
        hostNames[visitHostname] = hostNames[visitHostname] + 1
        #print(hostNames[visitHostname])
    else:
        hostNames[visitHostname] = 1
        #print(hostNames[visitHostname])

conn.close()

visitList = []
for key, value in hostNames.items():
    visitList.append(value)

total = np.sum(visitList)

visitList = sorted(visitList, reverse=True)

plt.scatter(np.arange(len(visitList)), visitList)
plt.title('Distribution of visits to different hostnames')
plt.ylabel('visits')
plt.xlabel('sites')
plt.show()
