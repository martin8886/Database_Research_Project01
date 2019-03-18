from flask import Flask
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify
from flask import Flask, render_template, request, redirect
import logging
import NovaBackend

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
    # Check if HipparcosID is null
    try:
        # Check if they're entering a number less than or equal to 0.
        HipparcosID = int(request.form['HipparcosID'])
        if (HipparcosID < 1) or (HipparcosID > 113474): return redirect("localhost:5000/index.html")
    except:
        HipparcosID = None  # it was blank to begin with
    # Check if Constellation is null
    Constellation = request.form['Constellation']
    if Constellation == "": Constellation = None    # it was blank to begin with
    # Check if SpectralType is null
    SpectralType = request.form['SpectralType']
    if SpectralType == "": SpectralType = None      # it was blank to begin with
    # Check all 3 fields of RA (for now I'm only going to do 1 since it's all we have)
    try:
        RA_Hours = int(request.form['RA_Hours_Minutes_Seconds'])
        # Make sure RA_Hours is between 0-24
        if (RA_Hours < 0) or (RA_Hours > 24): return redirct("localhost:5000/index.html")
    except:
        RA_Hours = None     # it was blank to begin with
    # Check if Declination is null
    try:
        Dec = float(request.form['Dec'])
        # Then check if declination is between -90 and 90
        if (Dec > 90) or (Dec < -90): return redirct("localhost:5000/index.html")
    except:
        Dec = None          # it was blank to begin with
    # Check if Distance is null
    try:
        Distance = float(request.form['Distance'])
        # Make sure it's a positive distance
        if Distance < 0: return redirct("localhost:5000/index.html")
    except:
        Distance = None     # it was blank to begin with
    # Check if Magnitude is null
    Magnitude = request.form['Magnitude']
    if Magnitude == "":     # it was blank to begin with
        return redirct("localhost:5000/index.html")
    else:
        Magnitude = float(Magnitude)
    # Check if Absolute_Magnitude is null
    Absolute_Magnitude = request.form['Absolute_Magnitude']
    if Absolute_Magnitude == "":    # it was blank to begin with
        return redirct("localhost:5000/index.html")
    else:
        # Turn the string into a float
        Absolute_Magnitude = float(Absolute_Magnitude)
    # Check if Luminosity is null
    Luminosity = request.form['Luminosity']
    if Luminosity == "":    # it was blank to begin with
        return redirct("localhost:5000/index.html")
    else:
        # Turn the string into a float and make sure it's positive
        Luminosity = float(Luminosity)
        if Luminosity < 0: return redirct("localhost:5000/index.html")
    # Check if Min_Magnitude is null
    Min_Magnitude = request.form['Min_Magnitude']
    if Min_Magnitude == "":    # it was blank to begin with
        return redirct("localhost:5000/index.html")
    else:
        # Turn the string into a float
        Min_Magnitude = float(Min_Magnitude)
    # Check if Max_Magnitude is null
    Max_Magnitude = request.form['Max_Magnitude']
    if Max_Magnitude == "":
        return redirct("localhost:5000/index.html")
    else:
        # Turn the string into a float
        Max_Magnitude = float(Max_Magnitude)
    # Check if Star_System_Name is null
    Star_System_Name = request.form['Star_System_Name']
    if Star_System_Name == "": Star_System_Name = None      # it was blank to begin with
    # Check if CompanionID is null
    try:
        CompanionID = int(request.form['CompanionID'])
    except:
        CompanionID = None  # it was blank to begin with
    results = {"HipparcosID": HipparcosID, "Constellation": Constellation, "Spectral Type": SpectralType,
               "RA Hours": RA_Hours, "Dec": Dec, "Distance": Distance, "Magnitude": Magnitude,
               "Absolute Magnitude": Absolute_Magnitude, "Luminosity": Luminosity, "Min Magnitude": Min_Magnitude,
               "Max Magnitude": Max_Magnitude, "Star System Name": Star_System_Name, "Companions": CompanionID}
    query= NovaBackend.ParseQuery(results)
    print(query)
    return(jsonify(results))

## Starts the server for serving Rest Services
if __name__ == '__main__':
    app.run(debug=False)
