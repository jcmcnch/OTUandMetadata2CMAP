#!/bin/bash -i

if [[ ${#1} -eq 0 ]] ; then
    echo 'Please enter an informative name for the output table as the second argument after the script (no spaces).'
    exit 0
fi

conda activate opedia-env

metadata=00-metadata/sample-metadata.tsv

filestem=$1

mkdir 01-modified-tables/

for item in `ls 00-input-tables/*`; do

	cp $item 01-modified-tables

done

mkdir 02-output-CMAP/

for item in `ls 01-modified-tables/*`; do

	sed -i "1s/#OTU ID/eASV-ID/" $item
	#sed -i -re 's/Kingdom\.(\S+)/\1/g;s/Supergroup\S+//g;s/Phylum\.(\S+)/\1/g;s/Class\.(\S+)/\1/g;s/Subclass\S+//g;s/Order\.(\S+)/\1/g;s/Suborder\S+//g;s/Family\.(\S+)/\1/g;s/Genus\.(\S+)/\1/g;s/Species\.(\S+)/\1/g' $item #transform PhytoRef to 7 levels
	sed -i 's/Eukaryota; /Chloroplast-/g' $item #remove first column from PhytoRef new taxonomy to make sure it's only 7 levels

	./OTUandMetadata2CMAP/scripts/convert-table-and-metadata-to-CMAP.py --input_normalized $item --input_metadata $metadata --output_cmap 02-output-CMAP/$filestem.CMAP.tsv


done

conda deactivate
