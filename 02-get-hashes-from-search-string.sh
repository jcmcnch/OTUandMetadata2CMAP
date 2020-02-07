#!/bin/bash

if [[ ${#1} -eq 0 ]] ; then
    echo 'Please enter a search string.'
    exit 0
fi

for hash in `grep $1 abund-filtered-tables/*tsv | cut -f1` ; do 

	searchString=$1

	printf "$hash\t$1\n"

done > hashes/$1.tsv
