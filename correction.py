from better_profanity import profanity
from textblob import TextBlob
from gramformer import Gramformer
import pandas as pd

# Define Functions to filter profanity, and correct spelling and grammar in text.
def add_profanity_prediction(text):
    return profanity.contains_profanity(text)

def correct_spelling(text):
    return str(TextBlob(text).correct())

def correct_grammar(text):
    corrected_text = gf.correct(text)
    return corrected_text

# Read the CSV file into a pandas DataFrame
input_csv = r"C:\Users\IGTPC\OneDrive\Desktop\sample11thOct.csv" 
df = pd.read_csv(input_csv)

# Create new columns for corrected versions
df['Corrected Spelling'] = ""
df['Corrected Grammar'] = ""
df['Profanity'] = ""

# Load Gramformer to correct grammar
gf = Gramformer(models=1, use_gpu=False) # 1=corrector, 2=detector

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
output_csv = "corrected_output1.csv"
df.to_csv(output_csv, index=False)
