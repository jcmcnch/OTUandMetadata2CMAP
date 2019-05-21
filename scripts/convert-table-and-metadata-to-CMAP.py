#!/usr/bin/env python3

import csv
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='This script takes an eASV spreadsheet generated from QIIME2, metadata indexed to the qiime2-ID, and a tsv spreadsheet with cluster membership to generate output for CMAP. The format is different from an OTU table in that each observation of an eASV at a particular location is treated as discrete oceanographic data points would be treated. So, each row is an abundance of an eASV at one particular location.')
parser.add_argument('--input_normalized', help='Your normalized tsv output from your biom spreadsheet, including taxonomy.')
parser.add_argument('--input_metadata', help='A tsv spreadsheet with the study metadata you wish to include. Must be indexed by qiime2-ID in a similar manner as described for sample-metadata.tsv in qiime2.')
parser.add_argument('--input_membership_summary', help='A tsv spreadsheet describing the membership of your clusters in the format centroid\tmember1,member2, ... ,memberN')
parser.add_argument('--output_cmap', help='Your output for CMAP as a tsv spreadsheet.')

args = parser.parse_args()

hashSamples = {}
hashSamplesHeader = ["ESV_ID_or_Cluster_Centroid", "qiime2-ID", "Relative_Abundance", "Study_Max_Abund", "Clustering_Level", "Cluster_Type", "Cluster_Members", "Num_Cluster_Members", "Domain", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
aTaxBlank = ["","","","","","",""]
boolClustCheck = True
strClustLevel = 100
strClustType = "None, deblur ESV"
strMembers = ""
iMembers = 0

hashMembership = {}

if args.input_membership_summary is not None: #If argument for
	for astrLine in csv.reader(open(args.input_membership_summary), csv.excel_tab):
		hashMembership[astrLine[0]] = astrLine[1]

handle = open(args.input_normalized)
aSamples = handle.readline().strip('\n').split('\t')[2:]

for astrLine in csv.reader(handle, delimiter='\t'):

	if boolClustCheck == True: #Do only once, get clustering level from ESV-ID
		if len(astrLine[0].split(';')) > 1:
			strClustLevel = astrLine[0].split(';')[1][0:2]
			strClustType = "VSEARCH clust. ESVs, %s pc ID" % strClustLevel
			boolClustCheck = False

	if len(astrLine[0].split(';')) > 1: #Check if plain ESV or cluster centroid

		strMembers = hashMembership[astrLine[0].split(';')[0]]
		iMembers = len(hashMembership[astrLine[0].split(';')[0]].split(',')) #Get string of membership from dict parsed from external file

	aAbund = np.array(astrLine[2:])
	aAbund = aAbund.astype(np.float)
	iStudyMax = np.amax(aAbund)

	hashKeys = []

	ESVid=astrLine[0]

	for i in range(len(aSamples)):

		uniquekey = aSamples[i] + ":" + ESVid #A unique key that combines sample and ESV

		hashKeys.append(uniquekey) #Add to an array

	for item in hashKeys: #Iterate over unique IDs

		abund = astrLine[ hashKeys.index(item) + 2 ] # Get abundance for ESV at particular station

		qiime2_ID = item.split(":")[0]
		hashSamples[item] = [ESVid, qiime2_ID, abund, iStudyMax, strClustLevel, strClustType, strMembers, iMembers] #add to dictionary

		counter = 0

		for i in range(len(astrLine[1].split(';'))): #Split out the taxonomic levels

			strToReplace = "D_" + str(i) + "__"
			hashSamples[item].append(astrLine[1].split(';')[i].replace(strToReplace,""))
			counter += 1

		for i in range(counter,7):
			hashSamples[item].append(aTaxBlank[i]) #Fill empty taxonomic identifiers with placeholders


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
