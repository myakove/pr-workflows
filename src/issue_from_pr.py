def issue_from_pr(repo, pull):
    issue_title = pull.title

    def _issue_exists():
        for _issue in repo.get_issues():
            if _issue.title == issue_title:
                return False

    if not _issue_exists():
        issue = repo.create_issue(issue_title)
        issue.add_to_assignees(issue.user)
        issue.create_comment(f"Address #{pull.number}")
