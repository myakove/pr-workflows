import contextlib
import os
import re

import yaml
from github.GithubException import UnknownObjectException

from src.constants import (
    LABEL_KEY_MAJOR,
    LABEL_KEY_MINOR,
    LABEL_KEY_PATCH,
    SEMVER,
    SEMVER_LABELS_SET,
    SEMVER_USER_INPUT_LABELS_MAP,
)


def get_pull_from_data(event_data, repo):
    pull_number = event_data.get("number")
    if not pull_number:
        pull_number = event_data.get("issue", {}).get("number")

    if not pull_number:
        pull_number = event_data.get("pull_request", {}).get("number")

    if pull_number:
        print(f"pull number is {pull_number}")
        with contextlib.suppress(UnknownObjectException):
            return repo.get_pull(number=pull_number)

    else:
        _pull, _ = get_pull_and_commit_by_commit_sha(event_data=event_data, repo=repo)
        return _pull


def get_pull_and_commit_by_commit_sha(event_data, repo):
    try:
        commit_sha = event_data["commits"][-1]["id"]
    except KeyError:
        commit_sha = event_data.get("commit", {}).get("sha")

    if commit_sha:
        print(f"Current commit sha is: {commit_sha}")
        for pull in repo.get_pulls():
            for commit in pull.get_commits():
                if commit.sha == commit_sha:
                    return pull, commit

    print(f"commit sha not found in {event_data}")
    return None, None


def get_last_commit(pull):
    return list(pull.get_commits())[-1]


def get_labels(pull):
    return [label.name for label in pull.get_labels()]


def remove_label(pull, label, labels_from_pull=None):
    if labels_from_pull is None:
        labels_from_pull = get_labels(pull=pull)

    if label in labels_from_pull:
        print(f"Remove {label} from {pull.title}")
        pull.remove_from_labels(label=label)


def add_label(pull, label):
    print(f"Adding {label} to {pull.title}")
    pull.add_to_labels(label)


def get_repo_approvers():
    with open("OWNERS", "r") as fd:
        data = yaml.load(stream=fd.read(), Loader=yaml.SafeLoader)

    return data["approvers"]


def print_os_environment():
    """
    Utility function for debugging.
    """
    for key, val in os.environ.items():
        print(f"{key}: {val}")


def semver_labels_exist_in_pull_labels(pull):
    return any([label in SEMVER_LABELS_SET for label in get_labels(pull=pull)])


def get_semver_user_input(body):
    match = re.match(
        rf".*\B/(?P<{SEMVER}>{LABEL_KEY_MAJOR}|{LABEL_KEY_MINOR}|{LABEL_KEY_PATCH})\b",
        body,
        re.IGNORECASE,
    )
    if match:
        return match.group(SEMVER).lower()


def get_semver_label_to_add_from_user_input(body):
    semver_user_input = get_semver_user_input(body=body)
    return SEMVER_USER_INPUT_LABELS_MAP.get(semver_user_input)


def add_remove_labels(pull, label_to_add, labels_to_remove, labels_from_pull):
    if label_to_add not in labels_from_pull:
        add_label(pull=pull, label=label_to_add)

    for label in labels_to_remove:
        if label in labels_from_pull:
            remove_label(pull=pull, label=label)
