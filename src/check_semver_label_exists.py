from src.constants import (
    BLOCK_MERGE_SEMVER_CONTEXT,
    STATE_PENDING,
    STATUS_DESCRIPTION_SEMVER_LABELS_MISSING,
)
from src.utils import get_last_commit, semver_labels_exist_in_pull_labels


def check_semver_label_exists(pull):
    if not semver_labels_exist_in_pull_labels(pull=pull):
        last_commit = get_last_commit(pull=pull)
        last_commit.create_status(
            state=STATE_PENDING,
            description=STATUS_DESCRIPTION_SEMVER_LABELS_MISSING,
            context=BLOCK_MERGE_SEMVER_CONTEXT,
        )
