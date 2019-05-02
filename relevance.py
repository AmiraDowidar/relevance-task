import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


## ================ Define Criteria =======================##
# size > 50,000 sf 
# large scale developments
# non residential
# 12 months
relevant_words = ['institutional', 'industerial', 'commercial', 'retail', 'mixed-use',
 'demolition', 'new', 'construction', 'large', 'campus', 'park', 'development']
irrelevant_words = ['condo','studios', 'residential', 'small', 'medium', 'legalize', 'administrative']
relevant_type = 'PRJ'

# with numeric values
project_duration = ['months', 'month', 'days', 'day']
project_size_sf = ['sf', 'gsf', 'squarefeet', 'square foot', 'square-foot']

# define stop words to eliminate from the list
stop_words = set(stopwords.words('english'))

## ================ Read data =======================##
# Import the filtered sheet into a Dataframe
data = pd.read_excel (r'city_notes.xlsx', 'filtered') 
df = pd.DataFrame(data, columns= ['OBJECTID','record_type_category','description'])

## ================ Filter data =======================##
# Remove null description rows as they 
df = df[df['description'].notnull()]
# Remove redundant data
df = df.drop_duplicates(subset='OBJECTID', keep='first')


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
    score+=sum(relevant_count.values())*10

    # get word count for irrelevant words and decrease their score
    irrelevant_count = { word: filtered_description.count(word) for word in irrelevant_words }
    score-=sum(irrelevant_count.values())*10

    # use regex to get approximate square feet
    # and increase score if relevant
    #check if list1 contains any elements in list2
    if any(e in filtered_description  for e in project_size_sf):
        p = re.compile(r'\d+ ')
        result = p.findall(' '.join(filtered_description))
        # result = re.search(r"(?=("+'|'.join(project_size_sf)+r"))", ' '.join(filtered_description))
        score+=len(result)*10

    # use regex to get duration
    if any(e in filtered_description  for e in project_duration):
        p = re.compile(r'\d+ ')
        result = p.findall(' '.join(filtered_description))
        # result = re.search(r"(?=("+'|'.join(size_sf)+r"))", ' '.join(filtered_description))
        score+=len(result)*10



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

# Save data to excel sheet
sorted_df.to_excel('data.xlsx', sheet_name='processed', index=False)

# Chart to visualize data
sorted_df = sorted_df[sorted_df['score'] > 150]
df_chart = sorted_df.plot.bar(x='OBJECTID', y='score', rot=0)
plt.show()
