
from pathlib import Path

from modules.evidence_collector import ALLOWED_ROOT


# -----------------------------------------
# VANISH - ERASURE VERIFICATION ENGINE
# -----------------------------------------


def evaluate_erasure(
    target_path,
    integrity_results,
    backup_checked=False,
    cloud_checked=False
):

    root = ALLOWED_ROOT.resolve()

    target = Path(target_path).expanduser().resolve(
        strict=False
    )

    # Restrict investigation to authorised evidence folder
    try:

        target.relative_to(root)

    except ValueError:

        return {
            "status": "INCONCLUSIVE",
            "reason": (
                "Target is outside the authorised evidence directory."
            )
        }

    if target == root:

        return {
            "status": "INCONCLUSIVE",
            "reason": "Select a file, not the evidence directory."
        }

    # Check whether the target currently exists
    if target.is_file():

        return {
            "status": "FAILED",
            "reason": (
                "The target file is still accessible at "
                "the investigated path."
            )
        }

    # Find historical evidence for this exact target
    matching_records = []

    for record in integrity_results:

        recorded_path = Path(
            record["file_path"]
        ).resolve(strict=False)

        if recorded_path == target:

            matching_records.append(record)

    # A historical SHA-256 baseline is required
    if not matching_records:

        return {
            "status": "INCONCLUSIVE",
            "reason": (
                "No historical evidence record exists for "
                "the specified target file."
            )
        }

    # Check whether baseline evidence is trustworthy
    for record in matching_records:

        if not record["original_hash"]:

            return {
                "status": "INCONCLUSIVE",
                "reason": "Historical SHA-256 baseline is missing."
            }

        if record["integrity_status"] in [
            "MODIFIED", "ERROR", "UNSTABLE"
        ]:

            return {
                "status": "INCONCLUSIVE",
                "reason": (
                    "An integrity anomaly was detected in "
                    "the historical evidence record."
                )
            }

    # Missing file is expected after the claimed deletion.
    # It does not prove complete sanitisation.

    if not backup_checked or not cloud_checked:

        return {
            "status": "PARTIALLY VERIFIED",
            "reason": (
                "The target is absent and a historical baseline "
                "exists, but backup and/or cloud evidence "
                "coverage is incomplete."
            )
        }

    # All defined prototype checks passed
    return {
        "status": "VERIFIED",
        "reason": (
            "The target is absent at the investigated path, "
            "a historical SHA-256 baseline exists, and the "
            "defined backup and cloud checks are marked complete. "
            "This conclusion is limited to the documented scope."
        )
    }
