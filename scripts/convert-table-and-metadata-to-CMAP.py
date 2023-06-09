#!/usr/bin/env python3

import csv
import pandas as pd
import numpy as np
import argparse
import re

parser = argparse.ArgumentParser(description='This script takes an eASV spreadsheet generated from QIIME2, metadata indexed to the qiime2-ID, and a tsv spreadsheet with cluster membership to generate output for CMAP. The format is different from an OTU table in that each observation of an eASV at a particular location is treated as discrete oceanographic data points would be treated. So, each row is an abundance of an eASV at one particular location.')
parser.add_argument('--input_normalized', help='Your normalized tsv output from your biom spreadsheet, including taxonomy.')
parser.add_argument('--input_metadata', help='A tsv spreadsheet with the study metadata you wish to include. Must be indexed by qiime2-ID in a similar manner as described for sample-metadata.tsv in qiime2.')
parser.add_argument('--input_membership_summary', help='A tsv spreadsheet describing the membership of your clusters in the format centroid\tmember1,member2, ... ,memberN')
parser.add_argument('--output_cmap', help='Your output for CMAP as a tsv spreadsheet.')

args = parser.parse_args()

hashSamples = {}
#hashSamplesHeader = ["ASV_ID_or_Cluster_Centroid", "qiime2-ID", "Relative_Abundance", "Study_Max_Abund", "Clustering_Level", "Cluster_Type", "Cluster_Members", "Num_Cluster_Members", "Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
hashSamplesHeader = ["ASV_hash", "qiime2-ID", "Relative_Abundance", "Study_Max_Abund", "Source_database", "Kingdom","Supergroup","Division","Domain","Phylum","Class","Order","Family", "Genus","Species"]
aTaxBlank = ["","","","","","","",""] #empty array for backfilling empty taxonomy strings
#boolClustCheck = True
#strClustLevel = 100
#strClustType = "None, DADA2 ASV"
#strMembers = ""
iMembers = 0

hashMembership = {}

if args.input_membership_summary is not None: #If argument for
        for astrLine in csv.reader(open(args.input_membership_summary), csv.excel_tab):
                hashMembership[astrLine[0]] = astrLine[1]

handle = open(args.input_normalized)
aSamples = handle.readline().strip('\n').split('\t')[2:]

for astrLine in csv.reader(handle, delimiter='\t'):

        """
        if boolClustCheck == True: #Do only once, get clustering level from ASV-ID
                if len(astrLine[0].split(';')) > 1:
                        strClustLevel = astrLine[0].split(';')[1][0:2]
                        strClustType = "VSEARCH clust. ASVs, %s pc ID" % strClustLevel
                        boolClustCheck = False

        if len(astrLine[0].split(';')) > 1: #Check if plain ASV or cluster centroid

                strMembers = hashMembership[astrLine[0].split(';')[0]]
                iMembers = len(hashMembership[astrLine[0].split(';')[0]].split(',')) #Get string of membership from dict parsed from external file
        """

        aAbund = np.array(astrLine[2:])
        aAbund = aAbund.astype(np.float)
        iStudyMax = np.amax(aAbund)

        hashKeys = []

        ASVid=astrLine[0]

        for i in range(len(aSamples)):

                uniquekey = aSamples[i] + ":" + ASVid #A unique key that combines sample and ASV

                hashKeys.append(uniquekey) #Add to an array

        for item in hashKeys: #Iterate over unique IDs

                abund = astrLine[ hashKeys.index(item) + 2 ] # Get abundance for ASV at particular station

                qiime2_ID = item.split(":")[0]

                #taxonomy string handling, assuming PR2 (8 levels) and SILVA (7 levels)
                #database versions hardcoded, change if needed
                taxonomy_string = astrLine[1]

                #Use regex to find PR2 taxonomy
                if re.match("Eukaryota", taxonomy_string.split(";")[0]):
                    taxArray = taxonomy_string.split(";")
                    taxArray = [x.strip(' ') for x in taxArray] #strip whitespace
                    for i in range(len(taxonomy_string.split(';')), 8): #Backfill empty taxonomic levels
                        taxArray.append(aTaxBlank[i])
                    #put blanks in the middle to leave space for SILVA tax
                    taxArray = ["PR2_4.14.0"] + taxArray[0:3] + ["", ""] + taxArray[3:]
		
		#same but for SILVA, with 7 levels instead of 8
                elif re.match("d__", taxonomy_string.split(";")[0]):
                    taxArray = taxonomy_string.split(";")
                    taxArray = [x.strip(' ') for x in taxArray] #strip whitespace
                    for i in range(len(taxonomy_string.split(';')), 7): #Backfill empty taxonomic levels
                        taxArray.append(aTaxBlank[i])
                    #put blanks at the beginning to leave space for PR2
                    taxArray = ["SILVA 138.1"] + ["", "", ""] + taxArray[0:]

                elif re.match("Unassigned", taxonomy_string.split(";")[0]):
                    taxArray = ["NA", "Unassigned", "", "", "", "", "", "", "", "", ""]

                hashSamples[item] = [ASVid, qiime2_ID, abund, iStudyMax] + taxArray #add to dictionary

firstLine = True
hashMetadata = {}

for astrLine in csv.reader(open(args.input_metadata), csv.excel_tab):

        if firstLine == True:
                aMetadataHeader = astrLine[1:]
                firstLine = False

        if firstLine == False:
                aCleanMetadata = astrLine[1:]
                aCleanMetadata[:] = [x.replace("−", "-") for x in aCleanMetadata]
                hashMetadata[astrLine[0]] = aCleanMetadata

for key in hashSamples.keys():

        concatArray = hashSamples[key] + hashMetadata[key.split(":")[0]][0:]
        hashSamples[key] = concatArray

hashSamplesHeader = hashSamplesHeader + aMetadataHeader

samplesDF = pd.DataFrame.from_dict(hashSamples, orient='index', columns=hashSamplesHeader)
samplesDF = samplesDF.apply(pd.to_numeric, errors='ignore')
cols = samplesDF.columns.tolist()
cols.insert(0, cols.pop(cols.index('depth')))
cols.insert(0, cols.pop(cols.index('lon')))
cols.insert(0, cols.pop(cols.index('lat')))
cols.insert(0, cols.pop(cols.index('time')))
samplesDF = samplesDF.reindex(columns=cols)
samplesDF = samplesDF.sort_values("Study_Max_Abund", axis=0, ascending=False)
samplesDF['time']=pd.to_datetime(samplesDF['time'], format='%Y-%m-%d %H:%M')
samplesDF.to_csv(args.output_cmap, encoding='utf-8', sep="\t", index=False)

handle.close()
