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
    if Constellation == "":
        Constellation = None    # it was blank to begin with
    else:
        if Constellation == "Andromeda": Constellation = "And"
        elif Constellation == "Antlia": Constellation = "Ant"
        elif Constellation == "Apus": Constellation = "Aps"
        elif Constellation == "Aquila": Constellation = "Aql"
        elif Constellation == "Aquarius": Constellation = "Aqr"
        elif Constellation == "Ara": Constellation = "Ara"
        elif Constellation == "Aries": Constellation = "Ari"
        elif Constellation == "Auriga": Constellation = "Aur"
        elif Constellation == "Bootes": Constellation = "Boo"
        elif Constellation == "Caelum": Constellation = "Cae"
        elif Constellation == "Camelopardalis": Constellation = "Cam"
        elif Constellation == "Capricornus": Constellation = "Cap"
        elif Constellation == "Carina": Constellation = "Car"
        elif Constellation == "Cassiopeia": Constellation = "Cas"
        elif Constellation == "Centaurus": Constellation = "Cen"
        elif Constellation == "Cepheus": Constellation = "Cep"
        elif Constellation == "Cetus": Constellation = "Cet"
        elif Constellation == "Chamaeleon": Constellation = "Cha"
        elif Constellation == "Circinus": Constellation = "Cir"
        elif Constellation == "Canis Major": Constellation = "Cma"
        elif Constellation == "Canis Minor": Constellation = "Cmi"
        elif Constellation == "Cancer": Constellation = "Cnc"
        elif Constellation == "Columba": Constellation = "Col"
        elif Constellation == "Coma Berenicies": Constellation = "Com"
        elif Constellation == "Corona Australis": Constellation = "Cra"
        elif Constellation == "Corona Borealis": Constellation = "Crb"
        elif Constellation == "Crater": Constellation = "Crt"
        elif Constellation == "Crux": Constellation = "Cru"
        elif Constellation == "Corvus": Constellation = "Crv"
        elif Constellation == "Canes Vanatici": Constellation = "Cvn"
        elif Constellation == "Cygnus": Constellation = "Cyg"
        elif Constellation == "Delphinus": Constellation = "Del"
        elif Constellation == "Dorado": Constellation = "Dor"
        elif Constellation == "Draco": Constellation = "Dra"
        elif Constellation == "Equuleus": Constellation = "Equ"
        elif Constellation == "Eridanus": Constellation = "Eri"
        elif Constellation == "Fornax": Constellation = "For"
        elif Constellation == "Gemini": Constellation = "Gem"
        elif Constellation == "Grus": Constellation = "Gru"
        elif Constellation == "Hercules": Constellation = "Her"
        elif Constellation == "Horologium": Constellation = "Hor"
        elif Constellation == "Hydra": Constellation = "Hya"
        elif Constellation == "Hydrus": Constellation = "Hyi"
        elif Constellation == "Indus": Constellation = "Ind"
        elif Constellation == "Lacerta": Constellation = "Lac"
        elif Constellation == "Leo": Constellation = "Leo"
        elif Constellation == "Lepus": Constellation = "Lep"
        elif Constellation == "Libra": Constellation = "Lib"
        elif Constellation == "Leo Minor": Constellation = "Lmi"
        elif Constellation == "Lupus": Constellation = "Lup"
        elif Constellation == "Lynx": Constellation = "Lyn"
        elif Constellation == "Lyra": Constellation = "Lyr"
        elif Constellation == "Mensa": Constellation = "Men"
        elif Constellation == "Microscopium": Constellation = "Mic"
        elif Constellation == "Monoceros": Constellation = "Mon"
        elif Constellation == "Musca": Constellation = "Mus"
        elif Constellation == "Norma": Constellation = "Nor"
        elif Constellation == "Octans": Constellation = "Oct"
        elif Constellation == "Ophiuchus": Constellation = "Oph"
        elif Constellation == "Orion": Constellation = "Ori"
        elif Constellation == "Pavo": Constellation = "Pav"
        elif Constellation == "Pegasus": Constellation = "Peg"
        elif Constellation == "Perseus": Constellation = "Per"
        elif Constellation == "Phoenix": Constellation = "Phe"
        elif Constellation == "Pictor": Constellation = "Pic"
        elif Constellation == "Piscis Austrinus": Constellation = "Psa"
        elif Constellation == "Pisces": Constellation = "Psc"
        elif Constellation == "Puppis": Constellation = "Pup"
        elif Constellation == "Pyxis": Constellation = "Pyx"
        elif Constellation == "Reticulum": Constellation = "Ret"
        elif Constellation == "Sculptor": Constellation = "Scl"
        elif Constellation == "Scropius": Constellation = "Sco"
        elif Constellation == "Scutum": Constellation = "Sct"
        elif Constellation == "Serpens Caput": Constellation = "Ser1"
        elif Constellation == "Serpens Cauda": Constellation = "Ser2"
        elif Constellation == "Sextans": Constellation = "Sex"
        elif Constellation == "Sagitta": Constellation = "Sge"
        elif Constellation == "Sagittarius": Constellation = "Sgr"
        elif Constellation == "Taurus": Constellation = "Tau"
        elif Constellation == "Telescopium": Constellation = "Tel"
        elif Constellation == "Triangulum Australe": Constellation = "Tra"
        elif Constellation == "Triangulum": Constellation = "Tri"
        elif Constellation == "Tucana": Constellation = "Tuc"
        elif Constellation == "Ursa Major": Constellation = "Uma"
        elif Constellation == "Ursa Minor": Constellation = "Umi"
        elif Constellation == "Vela": Constellation = "Vel"
        elif Constellation == "Virgo": Constellation = "Vir"
        elif Constellation == "Volans": Constellation = "Vol"
        else: Constellation = "Vul"
    # Check if SpectralType is null
    SpectralType = request.form['SpectralType']
    if SpectralType == "": SpectralType = None      # it was blank to begin with
    # Check all 3 fields of RA (for now I'm only going to do 1 since it's all we have)
    try:
        RA_Hours = int(request.form['RA_Hours_Minutes_Seconds'])
        # Make sure RA_Hours is between 0-24
        if (RA_Hours < 0) or (RA_Hours > 24): return redirect("localhost:5000/index.html")
    except:
        RA_Hours = None     # it was blank to begin with
    # Check if Declination is null
    try:
        Dec = float(request.form['Dec'])
        # Then check if declination is between -90 and 90
        if (Dec > 90) or (Dec < -90): return redirect("localhost:5000/index.html")
    except:
        Dec = None          # it was blank to begin with
    # Check if Distance is null
    try:
        Distance = float(request.form['Distance'])
        # Make sure it's a positive distance
        if Distance < 0: return redirect("localhost:5000/index.html")
    except:
        Distance = None     # it was blank to begin with
    # Check if Magnitude is null
    Magnitude = request.form['Magnitude']
    if Magnitude == "":     # it was blank to begin with
        Magnitude = None
    else:
        Magnitude = float(Magnitude)
    # Check if Absolute_Magnitude is null
    Absolute_Magnitude = request.form['Absolute_Magnitude']
    if Absolute_Magnitude == "":    # it was blank to begin with
        Absolute_Magnitude = None
    else:
        # Turn the string into a float
        Absolute_Magnitude = float(Absolute_Magnitude)
    # Check if Luminosity is null
    Luminosity = request.form['Luminosity']
    if Luminosity == "":    # it was blank to begin with
        Luminosity = None
    else:
        # Turn the string into a float and make sure it's positive
        Luminosity = float(Luminosity)
        if Luminosity < 0: return redirct("localhost:5000/index.html")
    # Check if Min_Magnitude is null
    Min_Magnitude = request.form['Min_Magnitude']
    if Min_Magnitude == "":    # it was blank to begin with
        Min_Magnitude = None
    else:
        # Turn the string into a float
        Min_Magnitude = float(Min_Magnitude)
    # Check if Max_Magnitude is null
    Max_Magnitude = request.form['Max_Magnitude']
    if Max_Magnitude == "":
        Max_Magnitude = None
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
    NovaBackend.MultiStarPlot(query)
    return(jsonify(results))

## Starts the server for serving Rest Services
if __name__ == '__main__':
    app.run(debug=False)
