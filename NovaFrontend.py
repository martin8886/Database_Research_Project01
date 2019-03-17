from flask import Flask
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify
from flask import Flask, render_template, request
import logging

# To Do list:
# 1) Design webpage appearance
#    Base it on the Layout Ideas.pptx
#    Install and learn visualization librarys as appropriate
# 2) Read in search criteria from webpage
# 3) Construct an SQL string that meets the search criteria
# 4) Query NovaDB with the constructed string
# 5) Post the query results to the appropriate page on the website
#    Single star: Star Summary Page
#    2 stars: Comparison Page
#    More than 2 stars: Star Map Page

app= Flask(__name__)    # Required to run the website

@app.route("/") # As soon as the website is loaded, it will direct to the index.html page.
def index():
    return render_template("index.html")

@app.route('/User_Query', methods=['POST'])
def User_Query():
    HipparcosID = request.form['HipparcosID']
    Constellation = request.form['Constellation']
    SpectralType = request.form['SpectralType']
    print(HipparcosID, " ", Constellation, " ", SpectralType)
    print(type(HipparcosID), " ", type(Constellation), " ", type(SpectralType))
    return(jsonify({"HipparcosID": HipparcosID, "Constellation": Constellation, "Spectral Type": SpectralType}))

## Starts the server for serving Rest Services
if __name__ == '__main__':
    app.run(debug=False)
