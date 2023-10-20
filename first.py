from better_profanity import profanity
import pandas as pd
from textblob import TextBlob
from language_tool_python import LanguageTool
import re

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', str(text))

def correct_spelling(text):
    return str(TextBlob(text).correct())

def correct_grammar(text):
    tool = LanguageTool('en-US')
    return str(tool.correct(text))

def add_profanity_prediction(text):
    return profanity.contains_profanity(text)

# Read the CSV file into a pandas DataFrame
input_csv = r"C:\Users\IGTPC\OneDrive\Desktop\sample11thOct.csv.xlsx" 
output_csv = "corrected_output1.csv"

#df = pd.read_csv(input_csv)
df = pd.read_excel(input_csv)

# Create new columns for corrected versions
df['Corrected Spelling'] = ""
#df['Corrected Grammar'] = ""
df['Profanity'] = ""

# Apply corrections conditionally based on the 'Role' column
for index, row in df.iterrows():
    if row['Role'] == 'User':
        profanity_check = add_profanity_prediction(row['Content'])
      #  cleaned_text = remove_punctuation(row['Content'])
        corrected_spelling_text = correct_spelling(row['Content'])
      # corrected_grammar_text = correct_grammar(corrected_spelling_text)
        # Update the new columns with corrected versions
        df.at[index, 'Corrected Spelling'] = corrected_spelling_text
      #  df.at[index, 'Corrected Grammar'] = corrected_grammar_text
        df.at[index, 'Profanity'] = profanity_check

# Save the corrected data to a new CSV file
df.to_csv(output_csv, index=False)
