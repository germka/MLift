#!/bin/sh

mkdir /home/germka/db_backup/tmp

pg_basebackup -D /home/germka/db_backup/tmp -F t -z -Z 9 -x -h localhost -p 5432 -U "postgres"

current_date='base_backup-'$(date '+%Y-%m-%d_%H:%M:%S')'.tar.gz'

mv /home/germka/db_backup/tmp/base.tar.gz /home/germka/db_backup/$current_date

rm -rf /home/germka/db_backup/tmp

exit 1