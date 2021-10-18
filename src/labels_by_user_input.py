from src.constants import (
    BLOCK_MERGE_SEMVER_CONTEXT,
    BLOCK_MERGE_VERIFY_CONTEXT,
    LABEL_APPROVE,
    LABEL_VERIFIED,
    NEEDS_MAINTAINERS_APPROVE,
    READY_FOR_MERGE,
    SEMVER_LABELS_SET,
    STATE_PENDING,
    STATE_SUCCESS,
    STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
    STATUS_DESCRIPTION_MISSING_VERIFIED,
    STATUS_DESCRIPTION_SEMVER_LABELS_EXIST,
)
from src.utils import (
    add_label,
    add_remove_labels,
    get_labels,
    get_last_commit,
    get_repo_approvers,
    get_semver_label_to_add_from_user_input,
    remove_label,
)


def labels_by_user_input(event_data, pull):
    commented_user = event_data["comment"]["user"]["login"]
    body = event_data["comment"]["body"]
    last_commit = get_last_commit(pull=pull)
    labels_from_pull = get_labels(pull=pull)

    if f"/{LABEL_VERIFIED}".lower() in body and LABEL_VERIFIED not in labels_from_pull:
        add_label(pull=pull, label=LABEL_VERIFIED)
        last_commit.create_status(
            state=STATE_SUCCESS,
            description="Verified label exists",
            context=BLOCK_MERGE_VERIFY_CONTEXT,
        )

    if f"/un{LABEL_VERIFIED}".lower() in body:
        remove_label(pull=pull, label=LABEL_VERIFIED, labels_from_pull=labels_from_pull)
        remove_label(
            pull=pull, label=READY_FOR_MERGE, labels_from_pull=labels_from_pull
        )

        last_commit.create_status(
            state=STATE_PENDING,
            description=STATUS_DESCRIPTION_MISSING_VERIFIED,
            context=BLOCK_MERGE_VERIFY_CONTEXT,
        )

    if commented_user in get_repo_approvers():

        if (
            f"/{LABEL_APPROVE}".lower() in body
            and LABEL_APPROVE not in labels_from_pull
        ):
            add_label(pull=pull, label=LABEL_APPROVE)
            last_commit.create_status(
                state=STATE_SUCCESS,
                description="Approved by maintainers",
                context=NEEDS_MAINTAINERS_APPROVE,
            )

        if f"/un{LABEL_APPROVE}".lower() in body:
            remove_label(
                pull=pull, label=LABEL_APPROVE, labels_from_pull=labels_from_pull
            )
            remove_label(
                pull=pull, label=READY_FOR_MERGE, labels_from_pull=labels_from_pull
            )

            last_commit.create_status(
                state=STATE_PENDING,
                description=STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL,
                context=NEEDS_MAINTAINERS_APPROVE,
            )

        semver_label_to_add = get_semver_label_to_add_from_user_input(body=body)
        if semver_label_to_add and semver_label_to_add not in labels_from_pull:
            add_remove_labels(
                pull=pull,
                label_to_add=semver_label_to_add,
                labels_to_remove=list(SEMVER_LABELS_SET - {semver_label_to_add}),
                labels_from_pull=labels_from_pull,
            )
            last_commit.create_status(
                state=STATE_SUCCESS,
                description=STATUS_DESCRIPTION_SEMVER_LABELS_EXIST,
                context=BLOCK_MERGE_SEMVER_CONTEXT,
            )
