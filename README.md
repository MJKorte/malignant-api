# malignant-api

This application takes variants from a JSON file and filters out all variants with an allele frequency > 0.1%. The database uses data that can be provided with gnomad standard VCF files. The application runs with docker and snakemake which allows the results to be easily reproducible on a linux system.


# Prerequisites
- snakemake
- docker
- python 3
- mySQL


# Setup
To run this application run inside malignant-api directory:

"docker-compose build"

"docker-compose up"

Be sure that the database and flask application are fully running (mySQL can take a while) before running:

"snakemake"


# explanation
The VCF_parser.py script searches for VCF files inside the "VCF_files" directory, gnomad files can be moved here. The file thats currently in the directory (test.vcf) contains the first 50 variants of the "gnomad.exomes.r2.1.1.sites.Y.vcf" file, because this file is 118MB I decided to make the file smaller otherwise Github wouldn't allow it. You can download gnomad files yourself to test this application. 

The variants that you want to filter need to be in the Input directory, the file name needs to be variants.json. To get an idea of the JSON format the API expects there is a variants.json included in this repository, a different type of array/object structure will not work!
