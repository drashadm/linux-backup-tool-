# Linux Backup Tool

A simple, secure, and modular backup script tailored for Linux environments such as Kali and is ideal for small businesses, schools, or home labs.

---

## Project Overview

This project simulates a real-world Linux backup automation process:
-  Archives critical files into timestamped ZIPs
-  Excludes unwanted file types (e.g. logs, temp files)
-  Logs every backup event into a structured `.csv`
-  Comes preloaded with sample data and GitHub Actions support

---


---

##  How to Test It Locally (Kali Linux)

```bash
# Make sure test folders exist
mkdir -p /home/kali/documents_to_backup
mkdir -p /home/kali/backups

# Add sample file to backup
echo "This is a test config file" > /home/kali/documents_to_backup/test.conf

# Run the backup tool
python3 linux_backup.py --source /home/kali/documents_to_backup --target /home/kali/backups
```

 Output:
- `backup_YYYYMMDD_HHMMSS.zip` in `/home/kali/backups`
- `backup_log.csv` showing status of each backup

---

## GitHub Actions: CI Automation

The workflow auto-runs the script when you push code to this repo.
Located in `.github/workflows/ci.yml`.

You can edit it to:
- Validate backup logic
- Simulate different scenarios
- Add test coverage (coming soon)

---

## Contact

This project is maintained by drashadm. For feedback, collaboration, or contract work — feel free to connect!

---

## Disclaimer

This tool is built for educational and demo purposes. Always test your backup setup before relying on it for production data.


_“Security is not a product, but a process.” — Bruce Schneier_
