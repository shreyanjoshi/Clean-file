import re
from textblob import TextBlob
from better_profanity import profanity
import pandas as pd
import sys
from gramformer import Gramformer

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', str(text))

def correct_spelling(text):
    return str(TextBlob(text).correct())

def correct_grammar(text):
    gf = Gramformer(models=1, use_gpu=False) # 1=corrector, 2=detector
    corrected_text = gf.correct(text)
    return corrected_text

def add_profanity_prediction(text):
    return profanity.contains_profanity(text)

# Read the CSV file into a pandas DataFrame
input_csv = r"C:\Users\IGTPC\OneDrive\Desktop\sample11thOct.csv" 
output_csv = "corrected_output1.csv"

df = pd.read_csv(input_csv)
#df = pd.read_excel(input_csv)
#df = pd.read_excel(input_csv, engine='openpyxl')

# Create new columns for corrected versions
df['Corrected Spelling'] = ""
df['Corrected Grammar'] = ""
df['Profanity'] = ""

# Apply corrections only for 'User' inputs under the 'Role' column
for index, row in df.iterrows():
    if row['Role'] == 'User':
        profanity_check = add_profanity_prediction(row['Content'])
        corrected_spelling_text = correct_spelling(row['Content'])
        corrected_grammar_text = correct_grammar(corrected_spelling_text)
        # Update the new columns with corrected versions
        df.at[index, 'Corrected Spelling'] = corrected_spelling_text
        df.at[index, 'Corrected Grammar'] = corrected_grammar_text
        df.at[index, 'Profanity'] = profanity_check

# Save the corrected data to a new CSV file
df.to_csv(output_csv, index=False)
