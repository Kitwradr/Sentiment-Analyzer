import operator
from collections import Counter
import json
import math
import globals as g 
from  globals import *
from collections import defaultdict
import os
import re

from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
import string

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except:
    from urllib import urlopen, urlencode # Python 2
 
stop = stopwords.words('english')
print(stop)