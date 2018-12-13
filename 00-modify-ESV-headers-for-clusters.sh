#!/bin/bash

for item in `ls *VSEARCH-clustered-ESVs*proportions.tsv`
	do
	clusteringlevel=`echo $item | grep -Eo "[[:digit:]]{2}pc"`
	gawk -v awkclusteringlevel="$clusteringlevel" -i inplace 'BEGIN{FS=OFS="\t"}{$1=$1";"awkclusteringlevel"-centroid"}1' $item
	sed -i "1s/#OTU ID;$clusteringlevel-centroid/ESV-ID/" $item
done
