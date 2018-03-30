try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except:
    from urllib import urlopen, urlencode # Python 2

import json

q = 'https://api.textgain.com/1/tag?' 
q += urlencode(dict(q='Salah scores a spectacular goal. Brilliant work from the man.', lang='en', key='***'))

r = urlopen(q)
r = r.read()
r = r.decode('utf-8')
r = json.loads(r)

partofspeechlist=r['text']
for sentence in partofspeechlist:
    for word in sentence:
        for actualword in word:
            if actualword['tag']=='ADJ':
                print(actualword)