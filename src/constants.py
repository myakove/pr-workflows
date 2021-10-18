BLOCK_MERGE_VERIFY_CONTEXT = "Verified label"

LABEL_VERIFIED = "Verified"
LABEL_APPROVE = "Approve"
NEEDS_MAINTAINERS_APPROVE = "Needs Maintainers Approve"
READY_FOR_MERGE = "Ready for merge"

STATE_SUCCESS = "success"
STATE_PENDING = "pending"

STATUS_DESCRIPTION_MISSING_VERIFIED = "Missing Verified (/verified)"
STATUS_DESCRIPTION_MISSING_MAINTAINERS_APPROVAL = "Needs /approve from maintainers"

SEMVER = "semver"

LABEL_KEY_MAJOR = "major"
LABEL_KEY_MINOR = "minor"
LABEL_KEY_PATCH = "patch"

BLOCK_MERGE_SEMVER_CONTEXT = f"{SEMVER} label".capitalize()
STATUS_DESCRIPTION_SEMVER_LABELS_EXIST = f"{SEMVER} label exists".capitalize()
STATUS_DESCRIPTION_SEMVER_LABELS_MISSING = f"Missing {SEMVER} label"

SEMVER_USER_INPUT_LABELS_MAP = {
    LABEL_KEY_MAJOR: f"{LABEL_KEY_MAJOR}/Breaking-Change".title(),
    LABEL_KEY_MINOR: f"{LABEL_KEY_MINOR}/Non-Breaking-Feature".title(),
    LABEL_KEY_PATCH: f"{LABEL_KEY_PATCH}/Non-Breaking-Fix".title(),
}
SEMVER_LABELS_SET = set(SEMVER_USER_INPUT_LABELS_MAP.values())
