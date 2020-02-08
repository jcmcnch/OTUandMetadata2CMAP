#!/bin/bash

mkdir -p plots filtered filtered/finished

for hash in `cat hashes/* | cut -f1`; do

	if find plots/ -name "*$hash*" -type f -printf 1 -quit | grep -q 1; then


		echo "Output already exists for $hash. Delete the output files if you want to rerun."
                mv filtered/$hash* filtered/finished

	else

                echo "Output graph does not exist yet for $hash. Filtering CMAP data to correct formatting and remove depths that will cause problems for interpolated plots."
                dataset-specific-filtering-GA03.sh $hash filtered

        fi

done
