import requests
import pandas as pd

# Replace these with your Bugzilla URL and API key
BUGZILLA_URL = 'https://bugzilla.mozilla.org'
API_KEY = 'a9HXRt56NcPZbvHFSNNvEopSLlabEBxIYTBt1GYG'

# Load CSV file
df = pd.read_csv('bug_comments_fixed.csv')

# Create a new column for the author ID, initializing with None
df['Author ID'] = None

# Counter for matches
match_counter = 0

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    email = row['Author']
    # /rest/user/{commenter}'
    user_profile_url = f'{BUGZILLA_URL}/rest/user/{email}'
    user_response = requests.get(user_profile_url, headers={'API-Key': API_KEY})
    user_data = user_response.json()

    # Check for successful response
    if 'users' in user_data and user_data['users']:
        user_info = user_data['users'][0]
        author_id = user_info.get('id', None)
        df.at[index, 'Author ID'] = author_id
        match_counter += 1
        
        # Print user details for debugging
        print(f"User ID for {email}: {author_id}")

        # Save every 100 matches
        if match_counter % 100 == 0:
            df.to_csv('id_bug_comments_fixed_partial_save.csv', index=False)
            print(f"Saved intermediate results after {match_counter} matches.")

# Save the updated DataFrame back to CSV
df.to_csv('id_bug_comments_fixed_final.csv', index=False)
