#!/bin/bash

source activate opedia-env

metadata=00-metadata/ANT28-5_Free-Living_0.2-3uM_fraction_with_counts_metadata.tsv

filestem="ANT-28-5_Free-Living_0.2-3uM_fraction"

for item in `ls 00-input-tables-clustered/*`; do

	cp $item 01-modified-tables-clustered

done

for item in `ls 01-modified-tables-clustered/*`; do

	../scripts/modify-ESV-headers-for-clusters.sh $item

	clusteringlevel=`echo $item | grep -Eo "[[:digit:]]{2}pc" | sed 's/pc//'`

	outputstem=`basename $item | awk -F"pc" '{$0=$1}1'`

	membership=`ls 00-cluster-membership/*summary*tsv | grep $clusteringlevel`

	../scripts/convert-table-and-metadata-to-CMAP.py --input_normalized $item --input_metadata $metadata --input_membership_summary $membership --output_cmap 02-output-CMAP/${outputstem}pc.CMAP.tsv

done

#for item in `ls $filestem* | grep -vE "summary|membership|metadata|VSEARCH|Opedia"`; do 

#	../scripts/convert-table-and-metadata-to-CMAP.py --input_normalized $item --input_metadata $metadata --output_cmap $filestem.CMAP.tsv

#done

conda deactivate
