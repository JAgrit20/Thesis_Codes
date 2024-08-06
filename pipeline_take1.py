import requests

# Replace these with your Bugzilla URL and API key
BUGZILLA_URL = 'https://bugzilla.mozilla.org'
API_KEY = 'a9HXRt56NcPZbvHFSNNvEopSLlabEBxIYTBt1GYG'
BUG_ID = '28286'  # Example bug ID

# Fetch bug details
bug_details_url = f'{BUGZILLA_URL}/rest/bug/{BUG_ID}'
response = requests.get(bug_details_url, headers={'API-Key': API_KEY})
bug_data = response.json()

# Check if the response contains the 'bugs' key and extract data
if 'bugs' in bug_data and bug_data['bugs']:
    bug = bug_data['bugs'][0]
    print(bug)

    # Extract commenter email addresses from the comments
    commenters = set()
    
    # Fetch comments associated with the bug
    comments_url = f'{BUGZILLA_URL}/rest/bug/{BUG_ID}/comment'
    comments_response = requests.get(comments_url, headers={'API-Key': API_KEY})
    comments_data = comments_response.json()

    # Check if the response contains the 'bugs' key and extract commenters
    if 'bugs' in comments_data and str(BUG_ID) in comments_data['bugs']:
        comments = comments_data['bugs'][str(BUG_ID)]['comments']
        for comment in comments:
            commenters.add(comment['creator'])

    # Fetch user details for each commenter
    for commenter in commenters:
        user_profile_url = f'{BUGZILLA_URL}/rest/user/{commenter}'
        user_response = requests.get(user_profile_url, headers={'API-Key': API_KEY})
        user_data = user_response.json()

        # Check for successful response
        if 'users' in user_data and user_data['users']:
            user_info = user_data['users'][0]
            print(user_info)
            # Print user details
            print(f"Name: {user_info.get('real_name', 'N/A')}")
            print(f"Email: {user_info.get('email', 'N/A')}")
            print(f"Creation Date: {user_info.get('creation_time', 'N/A')}")
            print(f"Last Activity Date: {user_info.get('last_activity_time', 'N/A')}")
            print(f"Can Login: {user_info.get('can_login', 'N/A')}")
            print(f"Comment Count: {user_info.get('comment_count', 'N/A')}")
            print(f"Bug Count: {user_info.get('bug_count', 'N/A')}")
        else:
            print(f"Error fetching details for user: {commenter}")

else:
    print("No bug data found.")
