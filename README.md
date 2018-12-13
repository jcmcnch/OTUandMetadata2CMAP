# OTUandMetadata2CMAP
A python script for converting a traditional OTU/eASV table and associated metadata into a format that can be ingested and queried easily by the Simons Foundation CMAP database.

Warning: This script will produce a very large output file, which is a redundant data format much larger than the traditional, compact "OTU table" (which it's still referred to even if some people are moving to eASVs). In some cases it might take up gigabytes of space on your computer so be aware of this before running it. If you gzip the resulting file it will be small enough to store though.

Also, make sure that your metadata is indexed by the same sample IDs that are included in your qiime2 output, otherwise it won't work.

The two associated bash scripts fix up the format of the OTU tables so that they are ready to parse by the python script. They remove an unnecessary header and add information to clustered eASVs to make sure that it's clear they're cluster centroids and not confused with the distribution of the single eASV.
