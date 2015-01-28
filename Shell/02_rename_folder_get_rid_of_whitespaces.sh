#!/bin/bash
for i in ./* ; do
  if [ -d "$i" ]; then
    echo "$i"
    b=$(echo $i | sed 's/ /_/g')
    echo "$b"
    mv "$i" "$b"
  fi
done
