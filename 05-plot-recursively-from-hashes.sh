#!/bin/bash

for item in filtered/*csv; do

	filestem=`basename $item | cut -d\. -f1`
	taxon=`grep -h $filestem hashes/* | cut -f2`

	c-microbial-map/scripts/plot.r -f $item -o plots -l $taxon.$filestem

done

for taxon in `ls plots/ | cut -d\. -f1 | sort | uniq` ; do

	mkdir -p plots/$taxon/other-plots
	mv plots/$taxon*png plots/$taxon/other-plots
	mv plots/$taxon/other-plots/*-03.png plots/$taxon

done
