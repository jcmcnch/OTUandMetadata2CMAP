#!/bin/bash

for item in filtered/*csv; do

	filestem=`basename $item | cut -d\. -f1`
	taxon=`grep -h $filestem hashes/* | cut -f2`
	study_max_abund=`cut -d, -f 8 $item | tail -n+2 | uniq`

	c-microbial-map/scripts/plot.r -f $item -o plots -l $taxon.max$study_max_abund.$filestem

done

for taxon in `ls plots/ | cut -d\. -f1 | sort | uniq` ; do

	mkdir -p plots/$taxon/other-plots
	mv plots/$taxon*png plots/$taxon/other-plots 2> /dev/null
	mv plots/$taxon/other-plots/*-03.png plots/$taxon 2> /dev/null

done
