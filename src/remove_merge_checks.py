from src.constants import LABEL_VERIFIED, READY_FOR_MERGE
from src.utils import remove_label


def remove_merge_checks(pull):
    remove_label(pull=pull, label=LABEL_VERIFIED)
    remove_label(pull=pull, label=READY_FOR_MERGE)
