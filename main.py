import requests
from datetime import datetime, timedelta
from prettytable import PrettyTable

# --- Settings ---
START_DATE = '2024-01-03' # Start date (YYYY-MM-DD)
OWNER = 'OWNER' # Repo owner
REPO = 'REPO' # Repo name
ACCESS_TOKEN = 'YOUR_TOKEN' # GitHub access token
# ---------------

def get_github_token():
    return ACCESS_TOKEN

def get_pull_requests_statistics(owner, repo):
    base_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {get_github_token()}'}

    params = {
        'state': 'all',
        'per_page': 100,  # Adjust as needed based on the number of pull requests
    }

    response = requests.get(base_url, headers=headers, params=params)
    pull_requests = response.json()

    user_statistics = {}

    # Initialize user statistics
    for pr in pull_requests:
        user = pr['user']['login']
        if user not in user_statistics:
            user_statistics[user] = {'created': 0, 'open': 0, 'required_reviews': 0, 'reviewed': 0, 'ignored': 0, 'average_review_time': 0, 'average_duration': 0}

    for pr in pull_requests:
        pr_owner = pr['user']['login']
        created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')

        # Check if the pull request is created after the start date
        if created_at >= datetime.strptime(START_DATE, '%Y-%m-%d'):

            user_statistics[pr_owner]['created'] += 1
            user_statistics[pr_owner]['open'] += 1 if pr['state'] == 'open' else 0

            # Get pull request reviews
            reviews_url = f"{pr['url']}/reviews"
            reviews_response = requests.get(reviews_url, headers=headers)
            reviews = reviews_response.json()
            reviewers = get_unique_reviewers(reviews)

            # Add reviewers to user statistics
            for reviewer in reviewers:
                if reviewer not in user_statistics:
                    user_statistics[reviewer] = {'created': 0, 'open': 0, 'required_reviews': 0, 'reviewed': 0, 'ignored': 0, 'average_review_time': 0, 'average_duration': 0}
                user_statistics[reviewer]['reviewed'] += 1

            # Calculate the average review time
            for review in reviews:
                reviewer_login = review['user']['login']
                reviewed_at = datetime.strptime(review['submitted_at'], '%Y-%m-%dT%H:%M:%SZ')
                user_statistics[reviewer_login]['average_review_time'] += calculate_duration(created_at, reviewed_at).total_seconds()

            # Calculate the average duration from creation to closing
            if pr['state'] == 'closed':
                closed_at = datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                duration = calculate_duration(created_at, closed_at)
                user_statistics[pr_owner]['average_duration'] += duration.total_seconds()

            # Process users from requested_reviewers
            for reviewer in pr['requested_reviewers']:
                reviewer_login = reviewer['login']
                if reviewer_login not in user_statistics:
                    user_statistics[reviewer_login] = {'created': 0, 'open': 0, 'required_reviews': 0, 'reviewed': 0, 'ignored': 0, 'average_review_time': 0, 'average_duration': 0}
                if pr['state'] == 'closed' and reviewer_login not in reviewers:
                    user_statistics[reviewer_login]['ignored'] += 1
                reviewers.add(reviewer_login)

            for reviewer_login in reviewers:
                user_statistics[reviewer_login]['required_reviews'] += 1

    # Calculate the average duration and review time
    for user, stats in user_statistics.items():
        if stats['created'] > 0:
            user_statistics[user]['average_duration'] /= stats['created']
            user_statistics[user]['average_duration'] = round(user_statistics[user]['average_duration'] / 3600, 2)
        if stats['reviewed'] > 0:
            user_statistics[user]['average_review_time'] /= stats['reviewed']
            user_statistics[user]['average_review_time'] = round(user_statistics[user]['average_review_time'] / 3600, 2)
        else:
            user_statistics[user]['average_review_time'] = 0

    return user_statistics

def calculate_duration(start_time, end_time):
    duration = end_time - start_time
    return duration

def get_unique_reviewers(reviews):
    unique_reviewers = set()
    for review in reviews:
        reviewer = review['user']['login']
        unique_reviewers.add(reviewer)
    return unique_reviewers

if __name__ == '__main__':
    owner = OWNER
    repo = REPO

    statistics = get_pull_requests_statistics(owner, repo)

    # Create statistic table
    statistic_table = PrettyTable()

    statistic_table.title = f"Pull Request Statistics for {owner}/{repo}"
    statistic_table.align = "l"
    statistic_table.field_names = ["User", "Created", "Open", "Required Reviews", "Reviewed", "Ignored", "Average Review Time (hours)", "Average Time To Close Own PRs (hours)"]
    for user, stats in statistics.items():
        statistic_table.add_row([
            user, stats['created'], stats['open'], stats['required_reviews'], stats['reviewed'], stats['ignored'], stats['average_review_time'], stats['average_duration']
        ])
    print(statistic_table.get_string(sortby="Required Reviews", reversesort=True))
