import requests
import math
from bs4 import BeautifulSoup

def calculate_comment_rating(data):
    experience_score = 1 - (data['last_activity_year'] - data['creation_year']) / data['creation_year']
    involvement_score = (data['comments_made'] + data['bugs_filed']) / (data['comments_made'] + data['bugs_filed'] + 1)
    expertise_score = (data['assigned_to'] + data['assigned_and_fixed']) / (data['assigned_to'] + data['assigned_and_fixed'] + 1)
    collaboration_score = (data['commented_on'] + data['patches_reviewed']) / (data['commented_on'] + data['patches_reviewed'] + 1)
    quality_score = (data['patches_submitted'] + data['bugs_poked']) / (data['patches_submitted'] + data['bugs_poked'] + 1)
    
    comment_rating = (0.2 * experience_score) + (0.25 * involvement_score) + (0.2 * expertise_score) + (0.15 * collaboration_score) + (0.2 * quality_score)
    
    return comment_rating

# URL of the user profile
url = 'https://bugzilla.mozilla.org/user_profile?user_id=599795'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract user details
    user_name = soup.select_one('div.vcard a').text.strip()
    creation_date = soup.select_one('tr:contains("Created") td:last-of-type').text.strip()
    last_activity = soup.select_one('tr:contains("Last activity") td:last-of-type').text.strip()
    
    # Handle possible null permissions field
    permissions_tag = soup.select_one('tr:contains("Permissions") td:last-of-type')
    permissions = permissions_tag.text.strip() if permissions_tag else "No permissions data"
    
    # Extract numeric statistics
    bugs_filed = int(soup.select_one('tr:contains("Bugs filed") td.numeric').text.strip())
    comments_made = int(soup.select_one('tr:contains("Comments made") td.numeric').text.strip())
    assigned_to = int(soup.select_one('tr:contains("Assigned to") td.numeric').text.strip())
    assigned_and_fixed = int(soup.select_one('tr:contains("Assigned to and fixed") td.numeric').text.strip())
    commented_on = int(soup.select_one('tr:contains("Commented on") td.numeric').text.strip())
    qa_contact = int(soup.select_one('tr:contains("QA-Contact") td.numeric').text.strip())
    patches_submitted = int(soup.select_one('tr:contains("Patches submitted") td.numeric').text.strip())
    patches_reviewed = int(soup.select_one('tr:contains("Patches reviewed") td.numeric').text.strip())
    bugs_poked = int(soup.select_one('tr:contains("Bugs poked") td.numeric').text.strip())
    
    # Handle possible empty last_activity
    if last_activity:
        last_activity_year = int(last_activity.split('-')[0])
    else:
        last_activity_year = 0  # or handle as needed
    
    creation_year = int(creation_date.split('-')[0])

    # Adjusted score calculations
    experience_score = math.log(1 + (last_activity_year - creation_year) / creation_year) if last_activity_year else 0
    involvement_score = math.sqrt(comments_made + bugs_filed) / (math.sqrt(comments_made + bugs_filed) + 1)
    expertise_score = (math.sqrt(assigned_to + assigned_and_fixed)) / (math.sqrt(assigned_to + assigned_and_fixed) + 1)
    collaboration_score = (math.sqrt(commented_on + patches_reviewed)) / (math.sqrt(commented_on + patches_reviewed) + 1)
    quality_score = (math.sqrt(patches_submitted + bugs_poked)) / (math.sqrt(patches_submitted + bugs_poked) + 1)

    # Updated weights
    weights = {
        'experience_score': 0.1,
        'involvement_score': 0.3,
        'expertise_score': 0.25,
        'collaboration_score': 0.2,
        'quality_score': 0.15
    }

    # Calculate weighted user score with penalty for inactivity
    current_year = 2024
    inactivity_penalty = 0 if last_activity_year == current_year else (current_year - last_activity_year) / 10

    user_score = (
        experience_score * weights['experience_score'] +
        involvement_score * weights['involvement_score'] +
        expertise_score * weights['expertise_score'] +
        collaboration_score * weights['collaboration_score'] +
        quality_score * weights['quality_score']
    ) - inactivity_penalty
        
    # Output the results
    print("User Name:", user_name)
    print("Created On:", creation_date)
    print("Last Activity:", last_activity)
    print("Permissions:", permissions)
    print("Bugs Filed:", bugs_filed)
    print("Comments Made:", comments_made)
    print("Assigned to:", assigned_to)
    print("Assigned to and Fixed:", assigned_and_fixed)
    print("Commented on:", commented_on)
    print("QA Contact:", qa_contact)
    print("Patches Submitted:", patches_submitted)
    print("Patches Reviewed:", patches_reviewed)
    print("Bugs Poked:", bugs_poked)
    
    # Output the scores
    print("\nScores:")
    print("Experience Score:", experience_score)
    print("Involvement Score:", involvement_score)
    print("Expertise Score:", expertise_score)
    print("Collaboration Score:", collaboration_score)
    print("Quality Score:", quality_score)
    print("\nOverall User Score:", user_score)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
