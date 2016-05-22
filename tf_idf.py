import math
from textblob import TextBlob as tb
from pymongo import MongoClient
from nltk.corpus import stopwords
import re
import string

class Example:
  def __init__(self, value):
    self.delta = value
  def gmm(self):
    self.delta += 1
    return self.delta

global king
king = Example(0)
count = 0
count2 = 0
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
  #   emoticons_str,
  #   r'<[^>]+>', # HTML tags
  #   r'(?:@[\w_]+)', # @-mentions
  #   r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
  #   r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 	# r'(?:[0-9]+)',
  #   r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[a-z][A-Z]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
stopwords_list = stopwords.words('english')
stopwords_list.append('via')
stopwords_list.append('rt')
stopwords_list.append('…')

for s in string.punctuation:
	stopwords_list.append(s)

for i in range(10):
	stopwords_list.append(str(i))

def tokenize(s):
	return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):	
	s = re.sub(r"http\S+", "", s)
	s = re.sub(r"https\S+", "", s)

	regex_punctuation = re.compile('[%s]' % re.escape(string.punctuation))
	s = regex_punctuation.sub('', s) # https://sudo.tw http ssudotw

	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	
	s = ' '
	word_list =  [w for w in tokens if w.lower() not in stopwords_list]
	result = s.join(word_list)	
	return result

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
	if count == 0:
		return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
	else:
		return math.log(count / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
	print(king.gmm())
	return tf(word, blob) * idf(word, bloblist)

bloblist = []
client = MongoClient('localhost:27017')
db = client.marvel

# for data in db.raw_data.find():
# 	processed_test = preprocess(data['text'], True)	
# 	tb_result = tb(processed_test)
# 	bloblist.append(tb_result)

all_content = ''

for data in db.raw_data.find():
	# processed_test = preprocess(data['text'], True)

	all_content = all_content + ' ' + data['text']
	count = count + 1
	if count == 500:
		break

# print(all_content)
bloblist.append(tb(preprocess(all_content, True)))
count2 = count
print(count)
for i, blob in enumerate(bloblist):
	print("Top words in document {}".format(i + 1))	
	scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
	print(scores)
	sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)	
	for word, score in sorted_words:
		print("\tWord: {}, TF-IDF: {}".format(word, score))

