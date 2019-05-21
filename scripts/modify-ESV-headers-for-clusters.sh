#!/bin/bash

clusteringlevel=`echo $1 | grep -Eo "[[:digit:]]{2}pc"`

gawk -v awkclusteringlevel="$clusteringlevel" -i inplace 'BEGIN{FS=OFS="\t"}{$1=$1";"awkclusteringlevel"-centroid"}1' $1

sed -i "1s/#OTU ID;${clusteringlevel}-centroid/ESV-ID/" $1
