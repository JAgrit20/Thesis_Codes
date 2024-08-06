import requests
import pandas as pd
from tqdm import tqdm  # for progress bar

# Replace these with your Bugzilla URL and API key
BUGZILLA_URL = 'https://bugzilla.mozilla.org'
API_KEY = 'a9HXRt56NcPZbvHFSNNvEopSLlabEBxIYTBt1GYG'

# Load CSV file
df = pd.read_csv('../bug_comments_fixed.csv')

# Create a new column for the author ID, initializing with None
df['Author ID'] = None

# Counter for matches
match_counter = 0

# Prepare an empty DataFrame to collect results for intermediate save
intermediate_results = pd.DataFrame()

# Iterate through each row in the DataFrame with a progress bar
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    email = row['Author']
    user_profile_url = f'{BUGZILLA_URL}/rest/user/{email}'
    try:
        user_response = requests.get(user_profile_url, headers={'API-Key': API_KEY})
        user_data = user_response.json()
        if 'users' in user_data and user_data['users']:
            user_info = user_data['users'][0]
            author_id = user_info.get('id', None)
            df.at[index, 'Author ID'] = author_id
            # Append the current row to intermediate results
            intermediate_results = pd.concat([intermediate_results, df.iloc[[index]]], ignore_index=True)
            match_counter += 1

            # Save to the same CSV every 10 matches
            if match_counter % 10 == 0:
                intermediate_results.to_csv('intermediate_bug_comments.csv', mode='a', header=False, index=False)
                intermediate_results = pd.DataFrame()  # Reset the DataFrame for the next batch
                print(f"Saved intermediate results after {match_counter} matches.")

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {email}: {e}")

# Save the updated DataFrame back to CSV
df.to_csv('id_bug_comments_fixed_final.csv', index=False)
