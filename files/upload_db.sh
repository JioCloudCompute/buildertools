#!/bin/bash

relpath() {
 python -c 'import os.path, sys;\
	print os.path.relpath(sys.argv[1], sys.argv[2])' "$1" "$2"
}

upload() {
  python uploadFileToS3.py "staging-database-backup" "$2" $1
}

file_list=`find $1`
for i in $file_list; do
  if [ -f $i ]; then
    upload $i `relpath $i $1`
  fi
done

