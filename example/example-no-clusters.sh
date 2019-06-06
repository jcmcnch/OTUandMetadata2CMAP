#!/bin/bash

source activate opedia-env

metadata=00-metadata/ANT28-5-Small-Particle-Associated_3-8uM_fraction_with_counts_metadata.tsv

filestem="ANT28-5_Small-Particle-Associated_3-8uM_fraction"

mkdir 01-modified-tables/

for item in `ls 00-input-tables/*`; do

	cp $item 01-modified-tables

done

mkdir 02-output-CMAP/

for item in `ls 01-modified-tables/*`; do

	sed -i "1s/#OTU ID/ESV-ID/" $item
	sed -i -re 's/Kingdom\.(\S+)/\1/g;s/Supergroup\S+//g;s/Phylum\.(\S+)/\1/g;s/Class\.(\S+)/\1/g;s/Subclass\S+//g;s/Order\.(\S+)/\1/g;s/Suborder\S+//g;s/Family\.(\S+)/\1/g;s/Genus\.(\S+)/\1/g;s/Species\.(\S+)/\1/g' $item

	../scripts/convert-table-and-metadata-to-CMAP.py --input_normalized $item --input_metadata $metadata --output_cmap 02-output-CMAP/$filestem.CMAP.tsv


done

conda deactivate
