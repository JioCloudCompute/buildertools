#!/bin/bash

upload() {
  filename=$(basename $2)
  ext="${filename##*.}"
  fname="${filename%.*}"
  python uploadFileToS3.py "staging-log-dir" "$1/`hostname`/`date +'%Y-%m-%d'`/$fname-`date +'%H%M%S'`.$ext" $2

}

file_list=`find $1|grep '[^zpo]$'`
for i in $file_list; do
  if [ -f $i ]; then 
    upload $2 $i
  fi  
done

