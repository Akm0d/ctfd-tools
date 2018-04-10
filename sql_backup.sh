#!/bin/bash

DB="${HOME}/CTFd/CTFd/ctfd.db"
BACKUPS="backups"

mkdir -p "${HOME}/$BACKUPS";

# If the database exists then dump it
if [ -f $DB ]; then
	NEW_BACKUP=$BACKUPS/ictf_`date '+%Y_%m_%d_%H_%M_%S'`.sq3
	echo "Backing up CTF to $NEW_BACKUP";
	sqlite3 $DB .dump > $NEW_BACKUP

	LAST_BACKUP=$BACKUPS/`ls -t $BACKUPS| head -n 2 |tail -n 1`

	if [ ! "$LAST_BACKUP" == "$NEW_BACKUP" ]; then
		echo "Last backup file: $LAST_BACKUP";
		H1=($(md5sum $LAST_BACKUP))
		H2=($(md5sum $NEW_BACKUP))

		echo "Checking for changes in Database";
		if [ "$H1" == "$H2" ]; then
			echo "No changes to databse, removing $NEW_BACKUP";
			rm $NEW_BACKUP;
		fi
	fi

else 
	echo "No database at $DB";
fi

# TODO Zip up backups if there get to be too many

