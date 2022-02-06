from src.constants import READY_FOR_MERGE
from src.utils import add_label, get_labels, remove_label


def merge_status_label(pull, commit):
    if not commit:
        print("No commit given")
        return

    print(pull)
    print(commit)
    if commit.get_combined_status().state == "success":
        add_label(pull=pull, label=READY_FOR_MERGE)
    else:
        if READY_FOR_MERGE in get_labels(pull=pull):
            remove_label(pull=pull, label=READY_FOR_MERGE)
