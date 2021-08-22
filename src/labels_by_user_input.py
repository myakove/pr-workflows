import re

from src.constants import LABEL_APPROVE, LABEL_VERIFIED, LABELS_DICT
from src.utils import (
    add_label,
    get_labels,
    get_repo_approvers,
    remove_label,
    set_commit_status_pending_no_approve,
    set_commit_status_pending_no_verify,
    set_commit_status_success_approve,
    set_commit_status_success_verify,
)


NEWLINE = "\n"

UNSUPPORTED_LABELS = f"""
You're trying to add/remove an unsupported label.
Supported labels -
{NEWLINE.join([f"/{key} to set {LABELS_DICT[key]}" for key in LABELS_DICT])}
To remove a label use '-', for example: /-<LABEL_NAME>
"""


def labels_by_user_input(data, pull, commented_user):
    body = data["comment"]["body"]
    commented_user = data["comment"]["user"]["login"]
    approver = commented_user in get_repo_approvers()
    pr_labels = get_labels(pull=pull)
    comment_labels = re.findall("(?:(?<=\\s)|(?<=^))/\\S*", body)

    for label in comment_labels:
        unlabel = label.startswith("/-")
        # If user label doesn't start with '/-', only '/' is stripped
        stripped_label = label.lower().lstrip("/-")

        if stripped_label not in LABELS_DICT:

            print(UNSUPPORTED_LABELS)
            return pull.create_comment(
                body=f"Hey @{commented_user},{UNSUPPORTED_LABELS}"
            )

        target_label = LABELS_DICT[stripped_label]
        verified = LABEL_VERIFIED in target_label
        approved = LABEL_APPROVE in target_label
        last_commit = list(pull.get_commits())[-1]

        if target_label in pr_labels and unlabel:

            if approved:
                set_commit_status_pending_no_approve(commit=last_commit)
                target_label = list(
                    (filter(lambda label: target_label in label, pr_labels))
                )[
                    0
                ]  # Extract correct approve label

            print(f"Removing {target_label} from {pull.title}")
            remove_label(pull=pull, label=target_label)

            if verified:
                set_commit_status_pending_no_verify(commit=last_commit)

        if target_label not in pr_labels and not unlabel:
            if approved:
                if not approver:
                    continue
                target_label = f"{commented_user}/{target_label}"
                set_commit_status_success_approve(commit=last_commit)

            print(f"Adding {target_label} to {pull.title}")
            add_label(pull=pull, label=target_label)

            if verified:
                set_commit_status_success_verify(commit=last_commit)
