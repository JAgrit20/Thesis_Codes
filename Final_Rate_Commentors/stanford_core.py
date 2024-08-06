import stanza

# Download the English model
stanza.download('en')

# Create a Stanza pipeline; this assumes you are using the English model.
nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,ner')

import pandas as pd

# Load your CSV file
df = pd.read_csv('../bug_comments.csv')
df = df[:10]

# Define a function to process text using Stanza
def process_text(text):
    doc = nlp(text)
    pos_tags = [(word.text, word.pos) for sent in doc.sentences for word in sent.words]
    ner_tags = [(ent.text, ent.type) for sent in doc.sentences for ent in sent.ents]
    return {'POS': pos_tags, 'NER': ner_tags}

# Apply the function to each row in the DataFrame
df['analysis'] = df['text'].apply(process_text)

# Print results
print(df[['text', 'analysis']])
