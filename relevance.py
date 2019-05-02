import pandas as pd
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


## ================ Define Criteria =======================##
# size > 50,000 sf 
# large scale developments
# non residential
# 12 months
relevant_words = ['institutional', 'industerial', 'commercial', 'retail', 'mixed-use', 'demolition', 'new', 'construction', 'large']
irrelevant_words = ['condo','studios', 'residential', 'small', 'medium']
relevant_type = 'PRJ'

# with numeric values
duration = ['months', 'month', 'days', 'day']
sf = ['sf', 'squarefeet', 'square feet']

# define stop words to eliminate from the list
stop_words = set(stopwords.words('english'))

## ================ Read data =======================##
# Import the filtered sheet into a Dataframe
data = pd.read_excel (r'city_notes.xlsx', 'filtered') 
df = pd.DataFrame(data, columns= ['OBJECTID','record_type_category','description'])

## ================ Filter data =======================##
# Remove null description rows as they 
df = df[df['description'].notnull()]


def getScore(filtered_description, type):
    """Return the project score based on the data in the description.

    Keyword arguments:
    filtered_description -- the filtered_description row in the data frame.
    type -- project type.
    """
    score = 0

    # increase score for projects with relevant type
    # and decrease score for projects with irrelevant type
    if type == relevant_type:
        score+=10
    else:
        score-=100

    
    # get word count for relevant words and increase their score
    relevant_count = { word: filtered_description.count(word) for word in relevant_words }

    # get word count for irrelevant words and decrease their score
    irrelevant_count = { word: filtered_description.count(word) for word in irrelevant_words }

    # use regex to get approximate square feet
    # and increase score if relevant

    # use regex to get duration


    # Calculate frequency distribution
    # fdist = nltk.FreqDist(filtered_words)


    return  score



def filterDescription(description):
    """Return the filtered desciption.

    Keyword arguments:
    description -- the description row in the data frame.
    """
    # Tokenize the description
    word_tokens = word_tokenize(description)
    # Make all words lower case
    filtered_words = [w.lower() for w in word_tokens]
    # Remove stop words
    filtered_words = [w for w in filtered_words if not w in stop_words]
    # Remove single chars like punctuation but leave numbers
    filtered_words = [w for w in filtered_words if len(w) > 1 or w.isnumeric()]

    return filtered_words


df['filtered_description'] = df.apply(lambda row: filterDescription(row['description']), axis = 1)

df['score'] = df.apply(lambda row: getScore(row['filtered_description'], row['record_type_category']), axis = 1)

# Sort df by score column in desc value
sorted_df = df.sort_values(by=('score'), ascending=False)
print(sorted_df)
