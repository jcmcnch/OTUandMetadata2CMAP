#!/bin/bash

source activate opedia-env

metadata=00-metadata/ANT28-5_Free-Living_0.2-3uM_fraction_with_counts_metadata.tsv

filestem="ANT-28-5_Free-Living_0.2-3uM_fraction"

mkdir 01-modified-tables-clustered

for item in `ls 00-input-tables-clustered/*`; do

	cp $item 01-modified-tables-clustered

done

mkdir 02-output-CMAP/

for item in `ls 01-modified-tables-clustered/*`; do

	../scripts/modify-ESV-headers-for-clusters.sh $item

	sed -i -re 's/Kingdom\.(\S+)/\1/g;s/Supergroup\S+//g;s/Phylum\.(\S+)/\1/g;s/Class\.(\S+)/\1/g;s/Subclass\S+//g;s/Order\.(\S+)/\1/g;s/Suborder\S+//g;s/Family\.(\S+)/\1/g;s/Genus\.(\S+)/\1/g;s/Species\.(\S+)/\1/g' $item #transform PhytoRef to 7 levels

	clusteringlevel=`echo $item | grep -Eo "[[:digit:]]{2}pc" | sed 's/pc//'`

	outputstem=`basename $item | awk -F"pc" '{$0=$1}1'`

	membership=`ls 00-cluster-membership/*summary*tsv | grep $clusteringlevel`

	../scripts/convert-table-and-metadata-to-CMAP.py --input_normalized $item --input_metadata $metadata --input_membership_summary $membership --output_cmap 02-output-CMAP/${outputstem}pc.CMAP.tsv

done

conda deactivate
