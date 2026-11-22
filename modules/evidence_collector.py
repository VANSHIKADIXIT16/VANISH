
import hashlib
import sqlite3
import uuid

from pathlib import Path
from datetime import datetime, timezone


# -----------------------------------------
# VANISH EVIDENCE COLLECTION ENGINE
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_DIR / "database" / "vanish.db"

ALLOWED_ROOT = PROJECT_DIR / "evidence"


# -----------------------------------------
# 1. DATABASE INITIALISATION
# -----------------------------------------

def initialise_database():

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(DATABASE_PATH) as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id TEXT PRIMARY KEY,
                scan_id TEXT,
                file_name TEXT,
                file_path TEXT,
                extension TEXT,
                size_bytes INTEGER,
                created_time TEXT,
                modified_time TEXT,
                collected_time TEXT,
                sha256 TEXT,
                collection_status TEXT,
                error_message TEXT
            )
        """)

        conn.commit()


# -----------------------------------------
# 2. SHA-256 CALCULATION
# -----------------------------------------

def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for chunk in iter(
            lambda: file.read(1024 * 1024), b""
        ):

            sha256.update(chunk)

    return sha256.hexdigest()


# -----------------------------------------
# 3. TIMESTAMP CONVERSION
# -----------------------------------------

def format_timestamp(timestamp):

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc
    ).isoformat()


# -----------------------------------------
# 4. CHECK AUTHORISED SCAN LOCATION
# -----------------------------------------

def validate_folder(folder_path):

    root = ALLOWED_ROOT.resolve()
    selected = Path(folder_path).expanduser().resolve(
        strict=True
    )

    if not selected.is_dir():
        raise ValueError("Selected path is not a directory.")

    try:
        selected.relative_to(root)

    except ValueError:
        raise ValueError(
            "For safety, VANISH can only scan folders "
            "inside its authorised evidence directory."
        )

    return selected


# -----------------------------------------
# 5. COLLECT FILE METADATA
# -----------------------------------------

def collect_file(file_path, scan_id):

    evidence_id = str(uuid.uuid4())

    collected_time = datetime.now(
        timezone.utc
    ).isoformat()

    try:

        # Capture metadata before hashing
        before = file_path.stat()

        sha256 = calculate_sha256(file_path)

        # Capture metadata again after hashing
        after = file_path.stat()

        # Check whether the file changed during collection
        if (
            before.st_size != after.st_size
            or before.st_mtime_ns != after.st_mtime_ns
        ):

            status = "UNSTABLE"
            error = "File metadata changed during collection."

        else:

            status = "COLLECTED"
            error = None

        # macOS birth time when available
        created_time = format_timestamp(
            getattr(before, "st_birthtime", before.st_ctime)
        )

        modified_time = format_timestamp(
            before.st_mtime
        )

        return {
            "evidence_id": evidence_id,
            "scan_id": scan_id,
            "file_name": file_path.name,
            "file_path": str(file_path),
            "extension": file_path.suffix.lower(),
            "size_bytes": before.st_size,
            "created_time": created_time,
            "modified_time": modified_time,
            "collected_time": collected_time,
            "sha256": sha256,
            "collection_status": status,
            "error_message": error
        }

    except (OSError, PermissionError) as error:

        return {
            "evidence_id": evidence_id,
            "scan_id": scan_id,
            "file_name": file_path.name,
            "file_path": str(file_path),
            "extension": file_path.suffix.lower(),
            "size_bytes": None,
            "created_time": None,
            "modified_time": None,
            "collected_time": collected_time,
            "sha256": None,
            "collection_status": "ERROR",
            "error_message": str(error)
        }


# -----------------------------------------
# 6. SAVE EVIDENCE INTO SQLITE
# -----------------------------------------

def save_evidence(records):

    with sqlite3.connect(DATABASE_PATH) as conn:

        conn.executemany("""
            INSERT INTO evidence (
                evidence_id,
                scan_id,
                file_name,
                file_path,
                extension,
                size_bytes,
                created_time,
                modified_time,
                collected_time,
                sha256,
                collection_status,
                error_message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                record["evidence_id"],
                record["scan_id"],
                record["file_name"],
                record["file_path"],
                record["extension"],
                record["size_bytes"],
                record["created_time"],
                record["modified_time"],
                record["collected_time"],
                record["sha256"],
                record["collection_status"],
                record["error_message"]
            )
            for record in records
        ])

        conn.commit()


# -----------------------------------------
# 7. SCAN SELECTED FOLDER
# -----------------------------------------

def scan_folder(folder_path):

    initialise_database()

    selected_folder = validate_folder(folder_path)

    scan_id = str(uuid.uuid4())

    records = []

    for current_folder in selected_folder.rglob("*"):

        try:

            # Do not follow or collect symbolic links
            if current_folder.is_symlink():
                continue

            if not current_folder.is_file():
                continue

            record = collect_file(
                current_folder,
                scan_id
            )

            records.append(record)

        except OSError as error:

            records.append({
                "evidence_id": str(uuid.uuid4()),
                "scan_id": scan_id,
                "file_name": current_folder.name,
                "file_path": str(current_folder),
                "extension": current_folder.suffix.lower(),
                "size_bytes": None,
                "created_time": None,
                "modified_time": None,
                "collected_time": datetime.now(
                    timezone.utc
                ).isoformat(),
                "sha256": None,
                "collection_status": "ERROR",
                "error_message": str(error)
            })

    if records:
        save_evidence(records)

    return records


# -----------------------------------------
# 8. RETRIEVE STORED EVIDENCE
# -----------------------------------------

def get_all_evidence():

    initialise_database()

    with sqlite3.connect(DATABASE_PATH) as conn:

        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT *
            FROM evidence
            ORDER BY collected_time DESC
        """).fetchall()

    return [dict(row) for row in rows]
