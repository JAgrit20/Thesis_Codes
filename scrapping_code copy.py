import requests
from bs4 import BeautifulSoup

# URL of the user profile
url = 'https://bugzilla.mozilla.org/user_profile?user_id=734788'

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
    permissions = soup.select_one('tr:contains("Permissions") td:last-of-type').text.strip()
    
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

    # Calculate scores
    current_year = 2024
    creation_year = int(creation_date.split('-')[0])
    last_activity_year = int(last_activity.split('-')[0])
    
    experience_score = 1 - (last_activity_year - creation_year) / creation_year
    involvement_score = (comments_made + bugs_filed) / (comments_made + bugs_filed + 1)
    expertise_score = (assigned_to + assigned_and_fixed) / (assigned_to + assigned_and_fixed + 1)
    collaboration_score = (commented_on + patches_reviewed) / (commented_on + patches_reviewed + 1)
    quality_score = (patches_submitted + bugs_poked) / (patches_submitted + bugs_poked + 1)
    
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
