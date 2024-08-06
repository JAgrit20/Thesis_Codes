import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from dateutil import parser

def fetch_user_details(author_id):
    # URL of the user profile
    url = f'https://bugzilla.mozilla.org/user_profile?user_id={int(author_id)}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            user_name = soup.select_one('div.vcard a').text.strip()
            creation_date = soup.select_one('tr:contains("Created") td:last-of-type').text.strip().split(' ')[0]
            last_activity = soup.select_one('tr:contains("Last activity") td:last-of-type').text.strip().split(' ')[0]
            permissions = soup.select_one('tr:contains("Permissions") td:last-of-type').text.strip()
            bugs_filed = int(soup.select_one('tr:contains("Bugs filed") td.numeric').text.strip())
            comments_made = int(soup.select_one('tr:contains("Comments made") td.numeric').text.strip())
            assigned_to = int(soup.select_one('tr:contains("Assigned to") td.numeric').text.strip())
            assigned_and_fixed = int(soup.select_one('tr:contains("Assigned to and fixed") td.numeric').text.strip())
            commented_on = int(soup.select_one('tr:contains("Commented on") td.numeric').text.strip())
            qa_contact = int(soup.select_one('tr:contains("QA-Contact") td.numeric').text.strip())
            patches_submitted = int(soup.select_one('tr:contains("Patches submitted") td.numeric').text.strip())
            patches_reviewed = int(soup.select_one('tr:contains("Patches reviewed") td.numeric').text.strip())
            bugs_poked = int(soup.select_one('tr:contains("Bugs poked") td.numeric').text.strip())
            
            return {
                "User Name": user_name, "Created On": creation_date, "Last Activity": last_activity, 
                "Permissions": permissions, "Bugs Filed": bugs_filed, "Comments Made": comments_made, 
                "Assigned to": assigned_to, "Assigned to and Fixed": assigned_and_fixed, 
                "Commented on": commented_on, "QA Contact": qa_contact, "Patches Submitted": patches_submitted, 
                "Patches Reviewed": patches_reviewed, "Bugs Poked": bugs_poked
            }
        except Exception as e:
            print(f"Error processing data for user_id {author_id}: {e}")
            return None
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None

def calculate_scores(df):
    # Parse dates
    df['Created On'] = df['Created On'].apply(lambda x: parser.parse(x).date())
    df['Last Activity'] = df['Last Activity'].apply(lambda x: parser.parse(x).date())
    
    max_values = df[['Comments Made', 'Assigned to and Fixed', 'Commented on', 'Patches Submitted']].max()
    
    df['experience_score'] = 1 - ((2024 - pd.to_datetime(df['Created On']).dt.year) / (2024 - pd.to_datetime(df['Created On']).dt.year).max())
    df['involvement_score'] = df['Comments Made'] / max_values['Comments Made']
    df['expertise_score'] = df['Assigned to and Fixed'] / max_values['Assigned to and Fixed']
    df['collaboration_score'] = df['Commented on'] / max_values['Commented on']
    df['quality_score'] = df['Patches Submitted'] / max_values['Patches Submitted']

    # Apply exponentiation
    df['experience_score'] **= 2
    df['involvement_score'] **= 2
    df['expertise_score'] **= 2
    df['collaboration_score'] **= 2
    df['quality_score'] **= 2

    # Weights for each score
    weights = {
        'experience_score': 0.1,
        'involvement_score': 0.3,
        'expertise_score': 0.2,
        'collaboration_score': 0.2,
        'quality_score': 0.2
    }
    
    # Calculate weighted user score
    df['Overall User Score'] = (
        df['experience_score'] * weights['experience_score'] +
        df['involvement_score'] * weights['involvement_score'] +
        df['expertise_score'] * weights['expertise_score'] +
        df['collaboration_score'] * weights['collaboration_score'] +
        df['quality_score'] * weights['quality_score']
    )
    
    return df

# Read CSV file
data = pd.read_csv('id_bug_comments_fixed_partial_save.csv')

# List to hold results
results = []

# Iterate over rows in DataFrame
for index, row in data.iterrows():
    user_details = fetch_user_details(row['Author ID'])
    if user_details:
        results.append({**row.to_dict(), **user_details})
    
    # Save every 10 iterations
    if (index + 1) % 10 == 0:
        results_df = pd.DataFrame(results)
        results_df = calculate_scores(results_df)
        results_df.to_csv('take_2_output.csv', index=False)
        results = []

# Save remaining data
if results:
    results_df = pd.DataFrame(results)
    results_df = calculate_scores(results_df)
    results_df.to_csv('take_2_Scores_output.csv', index=False)

print("Data processing completed and saved to output.csv.")
