#!/bin/bash

for item in `ls *proportions.tsv | grep -v "VSEARCH"`
	do
	sed -i "1s/#OTU ID/ESV-ID/" $item
done
