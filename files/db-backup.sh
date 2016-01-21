cd /root/db-backup/AWSS3ConfigManager/configManager

#Create backup
tmpdir="/tmp/backup-`date +'%Y%d%m'`"
innobackupex --user={{ db_admin_user }} --password={{ db_admin_password }} $tmpdir
./upload_db.sh $tmpdir
rm -rf $tmpdir

