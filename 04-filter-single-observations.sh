#!/bin/bash

mkdir -p filtered/single-or-zero-observations

for item in filtered/*csv; do 

	count=`cut -d\, -f5 $item | tail -n+2 | awk '$1>0{c++} END{print c+0}'`

	if [ "$count" -lt 2 ]; then

		mv $item filtered/single-or-zero-observations

	fi	

done
