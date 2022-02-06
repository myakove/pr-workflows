import github


def add_reviewers(pull, reviewers):
    reviewers = [reviewer.strip() for reviewer in reviewers.split(",")]
    for reviewer in reviewers:
        try:
            print(f"Requesting review from {reviewer} for {pull.title}")
            pull.create_review_request(reviewers=[reviewer])
        except github.GithubException as exp:
            # author ot the user who pushed cannot be added as reviewers
            print(f"Failed to add {reviewer}: {exp}")
