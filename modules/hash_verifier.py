
import hashlib
from pathlib import Path

from modules.evidence_collector import get_all_evidence


# -----------------------------------------
# VANISH - HASH INTEGRITY VERIFIER
# -----------------------------------------


def calculate_current_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for chunk in iter(
            lambda: file.read(1024 * 1024), b""
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


# -----------------------------------------
# VERIFY A SINGLE EVIDENCE RECORD
# -----------------------------------------

def verify_record(record):

    file_path = Path(record["file_path"])

    original_hash = record["sha256"]

    result = {
        "evidence_id": record["evidence_id"],
        "file_name": record["file_name"],
        "file_path": str(file_path),
        "original_hash": original_hash,
        "current_hash": None,
        "integrity_status": "ERROR",
        "details": ""
    }

    try:

        if file_path.is_symlink():
            result["details"] = "File is now a symbolic link."
            return result

        if not file_path.is_file():
            result["integrity_status"] = "MISSING"
            result["details"] = (
                "File is no longer present at the recorded path."
            )
            return result

        if not original_hash:
            result["details"] = (
                "No original SHA-256 hash is available."
            )
            return result

        # Capture metadata before hashing
        before = file_path.stat()

        current_hash = calculate_current_hash(file_path)

        # Capture metadata after hashing
        after = file_path.stat()

        result["current_hash"] = current_hash

        # Check whether file changed during verification
        if (
            before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
        ):
            result["integrity_status"] = "UNSTABLE"
            result["details"] = (
                "File changed during verification."
            )

        elif current_hash == original_hash:

            result["integrity_status"] = "MATCH"
            result["details"] = (
                "Original and current SHA-256 hashes match."
            )

        else:

            result["integrity_status"] = "MODIFIED"
            result["details"] = (
                "Original and current SHA-256 hashes differ."
            )

    except OSError as error:

        result["integrity_status"] = "ERROR"
        result["details"] = str(error)

    return result


# -----------------------------------------
# VERIFY ALL STORED EVIDENCE
# -----------------------------------------

def verify_all_evidence():

    records = get_all_evidence()

    results = []

    for record in records:

        result = verify_record(record)

        results.append(result)

    return results
