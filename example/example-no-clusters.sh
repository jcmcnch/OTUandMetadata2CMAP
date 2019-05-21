#!/bin/bash

source activate opedia-env

metadata=00-metadata/ANT28-5_Free-Living_0.2-3uM_fraction_with_counts_metadata.tsv

filestem="ANT-28-5_Free-Living_0.2-3uM_fraction"

for item in `ls 00-input-tables/*`; do

	cp $item 01-modified-tables

done

for item in `ls 01-modified-tables/*`; do

	sed -i "1s/#OTU ID/ESV-ID/" $item

	../scripts/convert-table-and-metadata-to-CMAP.py --input_normalized $item --input_metadata $metadata --output_cmap 02-output-CMAP/$filestem.CMAP.tsv


done

conda deactivate
