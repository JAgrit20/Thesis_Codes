import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import math 

def fetch_user_details(author_id):
    # URL of the user profile
    url = f'https://bugzilla.mozilla.org/user_profile?user_id={int(author_id)}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            user_name = soup.select_one('div.vcard a').text.strip()
            creation_date = soup.select_one('tr:contains("Created") td:last-of-type').text.strip()
            last_activity = soup.select_one('tr:contains("Last activity") td:last-of-type').text.strip()
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
            
            # Calculating scores
            current_year = 2024
            creation_year = int(creation_date.split('-')[0])
            last_activity_year = int(last_activity.split('-')[0])
            # experience_score = 1 - (last_activity_year - creation_year) / creation_year
            # involvement_score = (comments_made + bugs_filed) / (comments_made + bugs_filed + 1)
            # expertise_score = (assigned_to + assigned_and_fixed) / (assigned_to + assigned_and_fixed + 1)
            # collaboration_score = (commented_on + patches_reviewed) / (commented_on + patches_reviewed + 1)
            # quality_score = (patches_submitted + bugs_poked) / (patches_submitted + bugs_poked + 1)

            experience_score = math.log(1 + (last_activity_year - creation_year) / creation_year) if last_activity_year else 0
            involvement_score = math.sqrt(comments_made + bugs_filed) / (math.sqrt(comments_made + bugs_filed) + 1)
            expertise_score = (math.sqrt(assigned_to + assigned_and_fixed)) / (math.sqrt(assigned_to + assigned_and_fixed) + 1)
            collaboration_score = (math.sqrt(commented_on + patches_reviewed)) / (math.sqrt(commented_on + patches_reviewed) + 1)
            quality_score = (math.sqrt(patches_submitted + bugs_poked)) / (math.sqrt(patches_submitted + bugs_poked) + 1)

            # Weights for each score
            weights = {
                'experience_score': 0.2,
                'involvement_score': 0.25,
                'expertise_score': 0.2,
                'collaboration_score': 0.15,
                'quality_score': 0.2
            }
            
            # Calculate weighted user score
            user_score = (
                experience_score * weights['experience_score'] +
                involvement_score * weights['involvement_score'] +
                expertise_score * weights['expertise_score'] +
                collaboration_score * weights['collaboration_score'] +
                quality_score * weights['quality_score']
            )
            
            return {
                "User Name": user_name, "Created On": creation_date, "Last Activity": last_activity, 
                "Permissions": permissions, "Bugs Filed": bugs_filed, "Comments Made": comments_made, 
                "Assigned to": assigned_to, "Assigned to and Fixed": assigned_and_fixed, 
                "Commented on": commented_on, "QA Contact": qa_contact, "Patches Submitted": patches_submitted, 
                "Patches Reviewed": patches_reviewed, "Bugs Poked": bugs_poked, "Overall User Score": user_score
            }
        except Exception as e:
            print(f"Error processing data for user_id {author_id}: {e}")
            return None
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None

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
        pd.DataFrame(results).to_csv('output.csv', index=False)
        results = []

# Save remaining data
if results:
    pd.DataFrame(results).to_csv('Scores_output.csv', index=False)

print("Data processing completed and saved to output.csv.")
