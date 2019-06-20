#!/usr/bin/env python

#file: VCFparser.py
#author: Mark de Korte
#date: 08-06-2019
#version 4.20
#
#In this script the files inside the directory "/VCF_files" are parsed and inserted into the database

import io
import os
import time
import pandas as pd
import numpy as np
import mysql.connector




db_exists = False
#This while loop makes sure the script will only attempt to insert variants when the database is set up inside docker
while db_exists == False:
    try:
        db = mysql.connector.connect(host="malignantapi_mysql_1", user="root", password="pwd", database="vdatabase")
        db.close()
        db_exists = True
    except:
        print("database not running yet, trying again in 10 seconds")
        time.sleep(10)

#all files inside of the VCF_files directory are parsed and put into the database
vcf_files = os.listdir("VCF_files")


def insert_variants(vcf_files):
    for vcf_file in vcf_files:
        p = "VCF_files/" + vcf_file
        #make pandas dataframe of vcf
        try:
            df = read_vcf(p)
        except(FileNotFoundError):
            print("VCF files weren't found inside the directory VCF_files")
        AFlist = []
        genesymbols = []
        genes = []
        unipaccs = []
        #extract necessary info out of the "INFO" column of the variants
        for inf in df["INFO"]:
            listj = inf.split(";")
            subs = "AC_popmax"
            vep = listj[-1]
            veps = vep.split('|')
            genesymbol = veps[3]
            gene = veps[4]
            unipacc = veps[31]
            res = listj[2].split("=")[1]
            #check if info is available
            if len(genesymbol) == 0:
                genesymbols.append("Not available")
            else:
                genesymbols.append(genesymbol)
            if len(gene) == 0:
                genes.append("Not available")
            else:
                genes.append(gene)
            if len(unipacc) ==0:
                unipaccs.append("Not available")
            else:
                unipaccs.append(unipacc)
            if len(res) == 0:
                AFlist.append(np.nan)
            else:
                AFlist.append(float(res))
        #add info to the dataframe
        df["allele_freq"] = AFlist
        df["gene_symbol"] = genesymbols
        df["gene"] = genes
        df["unip_acc"] = unipaccs
        df = df.dropna()
        #filter alleles under 0,1%
        df = df.loc[df["allele_freq"] <= 0.001]
        df = df.drop(['QUAL','FILTER', 'INFO'], axis=1)
        np_df = df.values
        #connect with DB
        try:
            db = mysql.connector.connect( host="malignantapi_mysql_1", user="root", password="pwd", database="vdatabase")
            cursor = db.cursor()
            cursor.execute("show tables;")
            data = cursor.fetchone()
        except:
            print("Cannot connect to database right now")
        rowcount = 0
        #for every row in filtered dataframe insert a new variant
        for row in np_df:
            rowcount += 1
            sql = "insert into Variants (Chromosome, Pos, ID, REF, ALT, AF, genesymbol, gene, uniprot_acc) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, tuple(row))
        db.commit()
        print("Insertion of variants from "+ vcf_file + " succesfull!")
        print(rowcount, "records inserted.")
        db.close()


#the function read_vcf was made by git-user: dceoy
#the code can be found here: https://gist.github.com/dceoy/99d976a2c01e7f0ba1c813778f9db744
def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})

#call
insert_variants(vcf_files)