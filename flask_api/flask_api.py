#file: flask_api.py
#author: Mark de Korte
#date: 08-06-2019
#version 2.0
#
#This script runs a basic flask server locally, the POST request gives a Json with variants as input and the API checks a database
#to see if a variant is present, found variants are returned in a Json file with additional information


import mysql.connector
from flask import Flask, request

flask_api = Flask(__name__)

@flask_api.route('/parseJSON', methods=['POST'])
def parseJSON():
    #get input json file
    data = request.get_json()
    variantslist = []
    #connect to DB
    try:
        db = mysql.connector.connect(host="malignantapi_mysql_1", user="root", password="pwd", database="vdatabase")
    except:
        print("API cannot connect to the database right now.")
    cursor = db.cursor()
    sqlreturns = []
    #search database for variants found in input Json
    for i in data["variants"]:
        entry = []
        entry.append(i["chrom"])
        entry.append(i["pos"])
        entry.append(i["ref"])
        entry.append(i["alt"])
        #Make SQL statement + variables
        variantslist.append(entry)
        sql = "SELECT * FROM Variants WHERE Chromosome = %s AND Pos = %s AND REF = %s AND ALT = %s;"
        cursor.execute(sql, tuple(entry))
        data = cursor.fetchall()
        sqlreturns.append(data)


    db.close()
    #Build a Json string with variants
    json_string = """{\n "variants_found": [\n\t     """
    for item in sqlreturns:
        #put every found variant in output Json
        if item != []:
            for r in item:
                json_string = json_string + """{
             "chrom": \""""+r[0]+"""\",
             "pos": """+str(r[1])+""",
             "ref": \""""+r[3]+"""\",
             "alt": \""""+r[4]+"""\",
             "AF": """+str(r[5])+""",
             "symbol": \""""+r[6]+"""\",
             "gene": \""""+r[7]+"""\",
             "uniprot_acc": \""""+r[8]+"""\"
             },
             """
    #cut off last indentation + comma
    json_string = json_string[:-15] + """
            ]
}"""
    db.close()
    #return json output
    return json_string

if __name__ == '__main__':
    flask_api.run(host='0.0.0.0')