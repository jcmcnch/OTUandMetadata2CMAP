#!/bin/bash

hash=$1
outfolder=$2

mkdir -p raw

#get subset of data output using unique ASV hash or centroid hash
grep $hash 02-output-CMAP/*.tsv | awk -F $'\t' 'BEGIN {OFS = FS} {print $5,$2,$3,$4,$7,$20,$21,$8}' | sed 's/\t/,/g' > raw/$hash.cmap.csv

awk -F',' ' ($4 < 300 ) ' raw/$hash.cmap.csv > $outfolder/$hash.filtered.cmap.csv #Remove deeper depths for interpolation to work

sed -i '/23e0edad2f83d45f05720713885c2d39,,,,/d' $outfolder/$hash.filtered.cmap.csv #Need to remove station with few samples in order for interpolation to work

awk -F',' ' ($3 > 0 ) ' $outfolder/$hash.filtered.cmap.csv |  sort -g -k3 -t, > tmp1
awk -F',' ' ($3 < 0 ) ' $outfolder/$hash.filtered.cmap.csv |  sort -g -k3 -t, > tmp2

{ cat tmp1 ; cat tmp2 ; } | sponge $outfolder/$hash.filtered.cmap.csv #Sort longitude in natural way - damn you dateline

{ echo "centroid,latitude,longitude,depth,relative_abundance,temperature,salinity,study_max_abund" ; cat $outfolder/$hash.filtered.cmap.csv ; } | sponge $outfolder/$hash.filtered.cmap.csv #add header

rm tmp1 tmp2
