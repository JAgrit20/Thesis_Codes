import pandas as pd

# Load the data
data = pd.read_csv('bug_comments.csv')

# Define keywords for each category based on your specification
keywords = {
    'Clarification Requests': ['clarify', 'clarification', 'explain', 'unclear', 'confused'],
    'Reproduction Attempts': ['reproduce', 'reproduction', 'replicated', 'occurred again', 'can you reproduce', 'does it reproduce', 'reproduces', 'not able to reproduce'],
    'Additional Information': ['attachment', 'screenshot', 'log', 'update', 'additional info', 'error log', 'more info needed', 'additional details'],
    'Resolution/Workarounds': ['workaround', 'resolve', 'solution', 'fixed', 'temporary fix', 'fix the issue', 'solution found', 'resolved', 'is it fixed', 'try this fix'],
    'General Discussion': ['issue', 'problem', 'bug', 'error', 'fault', 'error reported', 'bug identified', 'problem encountered', 'issue persists'],
    'Assignment Requests': ['assign', 'take over', 'responsible', 'handle this', 'ownership', 'assign this bug', 'who will take this', 'assign to me']
}

def categorize_comment(text):
    if pd.isnull(text):
        return 'Uncategorized'  # Handle NaN or missing values
    
    category_scores = {category: 0 for category in keywords}
    
    for category, key_list in keywords.items():
        for key in key_list:
            if key in text.lower():
                category_scores[category] += 1
    
    # Select the category with the highest score
    max_score = max(category_scores.values())
    if max_score > 0:
        # Filter categories that match the max score
        selected_categories = [k for k, v in category_scores.items() if v == max_score]
        return ', '.join(selected_categories)
    return 'Uncategorized'

# Apply the categorization function
data['Category'] = data['Comment Text'].apply(categorize_comment)

# Save the categorized data to a new CSV file
output_file_path = 'categorized_comments.csv'
data.to_csv(output_file_path, index=False)

# output_file_path
