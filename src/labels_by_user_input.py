from src.constants import (
    BLOCK_MERGE_VERIFY_CONTEXT,
    LABEL_VERIFIED,
    READY_FOR_MERGE,
    STATE_PENDING,
    STATE_SUCCESS,
    STATUS_DESCRIPTION_MISSING_VERIFIED,
)
from src.utils import add_label, get_labels, remove_label


def labels_by_user_input(event_data, pull):
    body = event_data["comment"]["body"]
    last_commit = list(pull.get_commits())[-1]
    if f"/{LABEL_VERIFIED}".lower() in body and LABEL_VERIFIED not in get_labels(
        pull=pull
    ):
        add_label(pull=pull, label=LABEL_VERIFIED)
        last_commit.create_status(
            state=STATE_SUCCESS,
            description="Verified label exists",
            context=BLOCK_MERGE_VERIFY_CONTEXT,
        )

    if f"/un{LABEL_VERIFIED}".lower() in body:
        remove_label(pull=pull, label=LABEL_VERIFIED)
        remove_label(pull=pull, label=READY_FOR_MERGE)

        last_commit.create_status(
            state=STATE_PENDING,
            description=STATUS_DESCRIPTION_MISSING_VERIFIED,
            context=BLOCK_MERGE_VERIFY_CONTEXT,
        )
