import os
import shutil
import time
import zipfile
import argparse
import csv
from datetime import datetime

# === CONFIGURATION === #
EXCLUDE_EXTENSIONS = ['.log', '.tmp', '.bak']
DEFAULT_SOURCE = '/home/kali/documents_to_backup'
DEFAULT_TARGET = '/home/kali/backups'

# === FUNCTIONS === #

def log_backup(log_file, timestamp, status, details):
    file_exists = os.path.isfile(log_file)
    with open(log_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Timestamp', 'Status', 'Details'])
        writer.writerow([timestamp, status, details])

def should_exclude(file_path):
    return any(file_path.endswith(ext) for ext in EXCLUDE_EXTENSIONS)

def compress_backup(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname)
    shutil.rmtree(folder_path)

def create_backup(source_dir, backup_dir):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'backup_{timestamp}'
    backup_path = os.path.join(backup_dir, backup_name)
    log_file = os.path.join(backup_dir, 'backup_log.csv')

    try:
        os.makedirs(backup_path, exist_ok=True)

        for root, dirs, files in os.walk(source_dir):
            rel_root = os.path.relpath(root, source_dir)
            target_root = os.path.join(backup_path, rel_root)
            os.makedirs(target_root, exist_ok=True)

            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_root, file)
                if not should_exclude(file):
                    shutil.copy2(source_file, target_file)

        zip_file = f"{backup_path}.zip"
        compress_backup(backup_path, zip_file)

        log_backup(log_file, timestamp, 'Success', zip_file)
        print(f"[+] Backup complete and compressed to: {zip_file}")
    except Exception as e:
        log_backup(log_file, timestamp, 'Failed', str(e))
        print(f"[!] Backup failed: {e}")

# === MAIN === #
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Kali Linux Backup Tool")
    parser.add_argument('--source', default=DEFAULT_SOURCE, help='Folder to back up')
    parser.add_argument('--target', default=DEFAULT_TARGET, help='Backup destination folder')
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"[!] Source folder not found: {args.source}")
    elif not os.path.isdir(args.target):
        print(f"[!] Backup folder not found: {args.target}")
    else:
        create_backup(args.source, args.target)
