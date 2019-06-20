#file: snakefile
#author: Mark de Korte
#date: 10-06-2019
#This snakefile creates a workflow to filter variants, convert results to csv and make a report + workflow.svg


import json
import csv


#generate a workflow .svg
rule workflow:
	input:
		"Report/report.txt"
	output:
		"Report/workflow.svg"
	shell:
		"snakemake --dag {input} | dot -Tsvg > {output}"


#make a very basic report of variants found
rule make_report:
	input:
		"Input/variants.json",
		"Output/filtered_variants.csv"
	output:
		"Report/report.txt",
	run:
		 data = json.load(open(input[0]))
		 num_inp = len(data["variants"])
		 num_res = sum(1 for line in open(input[1])) -1
		 file = open(output[0], "w+")
		 file.write("Of the "+ str(num_inp) + " variants processed, "+ str(num_res)+ " were found to be possibly malignant with an allele frequency of < 0.1%.\n")
		 file.write("The found variants with their chromosome, position, mutation, allele frequency, gene and Uniprot accesion code can be found in the variants_filtered.json and variants_filtered.csv")
		 file.close()


#convert Json file from API to .csv file
rule to_csv:
	input:
		"Output/filtered_variants.json"
	output:
		"Output/filtered_variants.csv"
	run:
         file = open(input[0], "r")
         jsonc = json.load(file)
         csvw = csv.writer(open(output[0], "w", newline=''))
         csvw.writerow(["chrom", "pos", "ref", "alt", "AF", "symbol", "gene", "Uniprot_acc"])
         for entry in jsonc["variants_found"]:
             csvw.writerow([entry["chrom"], entry["pos"], entry["ref"], entry["alt"], entry["AF"], entry["symbol"], entry["gene"], entry["uniprot_acc"]])


#call api and receive filtered variants
rule filter_variants:
    input:
        "Input/variants.json"
    output:
        "Output/filtered_variants.json"
    shell:
        """curl -H "Content-Type: application/json" -d @{input} http://localhost:5000/parseJSON -o {output}"""






