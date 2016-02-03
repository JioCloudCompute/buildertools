#!/bin/bash -f
cd /root/log-backup/
mapfile -t logs < infiles
cd /root/log-backup/AWSS3ConfigManager/configManager

for log in "${logs[@]}"
do
  logfiles=`echo ${log}|awk '{print $1}'`
  folder=`echo ${log}|awk '{print $2}'`
  ./upload-log.sh $logfiles* $folder
done

