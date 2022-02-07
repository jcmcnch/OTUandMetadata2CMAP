#!/bin/bash

mkdir -p hashes

if [[ ${#1} -eq 0 ]] ; then
    echo 'Please enter a search string.'
    exit 0
fi

#search for target hashes in subsetted table
for hash in `grep $1 00-input-subsetted/*tsv | cut -f1` ; do 

	searchString=$1

	printf "$hash\t$1\n"

done > hashes/$1.tsv
