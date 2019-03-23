from flask import Flask
import pandas as pd
from flask import jsonify
from flask import Flask, render_template, request, redirect
import logging
import NovaBackend

# To Do list:
# 1) Design webpage appearance
#    Base it on the Layout Ideas.pptx                           -- DONE
#    Install and learn visualization librarys as appropriate    -- DONE
# 2) Read in search criteria from webpage                       -- DONE
# 3) Construct an SQL string that meets the search criteria     -- DONE
# 4) Query NovaDB with the constructed string                   -- DONE
# 5) Post the query results to the appropriate page on the website
#    Single star: Star Summary Page                             -- in progress
#    2 stars: Comparison Page                                   -- in progress
#    More than 2 stars: Star Map Page                           -- in progress

app= Flask(__name__, , static_url_path = "", static_folder = "templates")    # Required to run the website, file path for images added

@app.route("/") # As soon as the website is loaded, it will direct to the index.html page.
def index():
    return render_template("index.html")

@app.route('/User_Query', methods=['POST'])
def User_Query():
    # Read in the information entered into the web page
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
        # Otherwise, we need the 3 character ID instead of the fully spelled out name.  Hence...
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

    # Distance
    # Check if Distance_Lower is null
    try:
        Distance_Lower = float(request.form['Distance_Lower'])
        # Make sure it's a positive distance
        if Distance_Lower < 0: return redirect("localhost:5000/index.html")
    except:
        Distance_Lower = None     # it was blank to begin with
    # Check if Distance_Upper is null
    try:
        Distance_Upper = float(request.form['Distance_Upper'])
        # Make sure it's a positive distance
        if Distance_Upper < 0: return redirect("localhost:5000/index.html")
    except:
        Distance_Upper = None     # it was blank to begin with
    # Check that Distance_Upper is greater than Distance_Lower
    if (Distance_Lower != None) and (Distance_Upper != None):
        if Distance_Lower > Distance_Upper: return redirect("localhost:5000/index.html")

    # Coordinates (RA)
    # Check if RA_Lower is null
    try:
        RA_Lower = int(request.form['RA_Lower'])
        # Make sure RA_Lower is between 0-24
        if (RA_Lower < 0) or (RA_Lower > 24): return redirect("localhost:5000/index.html")
    except:
        RA_Lower = None     # it was blank to begin with
    # Check if RA_Upper is null
    try:
        RA_Upper = int(request.form['RA_Upper'])
        # Make sure RA_Upper is between 0-24
        if (RA_Upper < 0) or (RA_Upper > 24): return redirect("localhost:5000/index.html")
    except:
        RA_Upper = None     # it was blank to begin with
    # Check that RA_Upper is greater than RA_Lower
    if (RA_Lower != None) and (RA_Upper != None):
        if RA_Lower > RA_Upper: return redirect("localhost:5000/index.html")

    #Coordinates (Dec)
    # Check if Dec_Lower is null
    try:
        Dec_Lower = float(request.form['Dec_Lower'])
        # Then check if declination is between -90 and 90
        if (Dec_Lower > 90) or (Dec_Lower < -90): return redirect("localhost:5000/index.html")
    except:
        Dec_Lower = None          # it was blank to begin with
    # Check if Dec_Upper is null
    try:
        Dec_Upper = float(request.form['Dec_Upper'])
        # Then check if declination is between -90 and 90
        if (Dec_Upper > 90) or (Dec_Upper < -90): return redirect("localhost:5000/index.html")
    except:
        Dec_Upper = None          # it was blank to begin with
    # Check that Dec_Upper is greater than Dec_Lower
    if (Dec_Lower != None) and (Dec_Upper != None):
        if Dec_Lower > Dec_Upper: return redirect("localhost:5000/index.html")

    # Magnitude
    # Check if Magnitude_Lower is null
    Magnitude_Lower = request.form['Magnitude_Lower']
    if Magnitude_Lower == "":     # it was blank to begin with
        Magnitude_Lower = None
    else:
        Magnitude_Lower = float(Magnitude_Lower)
    # Check if Magnitude_Upper is null
    Magnitude_Upper = request.form['Magnitude_Upper']
    if Magnitude_Upper == "":     # it was blank to begin with
        Magnitude_Upper = None
    else:
        Magnitude_Upper = float(Magnitude_Upper)
    # Check that Magnitude_Upper is greater than Magnitude_Lower
    if (Magnitude_Lower != None) and (Magnitude_Upper != None):
        if Magnitude_Lower > Magnitude_Upper: return redirect("localhost:5000/index.html")

    # Absolute Magnitude
    # Check if Absolute_Magnitude_Lower is null
    Absolute_Magnitude_Lower = request.form['Absolute_Magnitude_Lower']
    if Absolute_Magnitude_Lower == "":     # it was blank to begin with
        Absolute_Magnitude_Lower = None
    else:
        Absolute_Magnitude_Lower = float(Absolute_Magnitude_Lower)
    # Check if Absolute_Magnitude_Upper is null
    Absolute_Magnitude_Upper = request.form['Absolute_Magnitude_Upper']
    if Absolute_Magnitude_Upper == "":     # it was blank to begin with
        Absolute_Magnitude_Upper = None
    else:
        Absolute_Magnitude_Upper = float(Absolute_Magnitude_Upper)
    # Check that Absolute_Magnitude_Upper is greater than Absolute_Magnitude_Lower
    if (Absolute_Magnitude_Lower != None) and (Absolute_Magnitude_Upper != None):
        if Absolute_Magnitude_Lower > Absolute_Magnitude_Upper: return redirect("localhost:5000/index.html")

    # Luminosity
    # Check if Luminosity_Lower is null
    Luminosity_Lower = request.form['Luminosity_Lower']
    if Luminosity_Lower == "":     # it was blank to begin with
        Luminosity_Lower = None
    else:
        Luminosity_Lower = float(Luminosity_Lower)
    # Check if Luminosity_Upper is null
    Luminosity_Upper = request.form['Luminosity_Upper']
    if Luminosity_Upper == "":     # it was blank to begin with
        Luminosity_Upper = None
    else:
        Luminosity_Upper = float(Luminosity_Upper)
    # Check that Luminosity_Upper is greater than Luminosity_Lower
    if (Luminosity_Lower != None) and (Luminosity_Upper != None):
        if Luminosity_Lower > Luminosity_Upper: return redirect("localhost:5000/index.html")

    # Minimum Variable Magnitude
    # Check if Min_Magnitude_Lower is null
    Min_Magnitude_Lower = request.form['Min_Magnitude_Lower']
    if Min_Magnitude_Lower == "":     # it was blank to begin with
        Min_Magnitude_Lower = None
    else:
        Min_Magnitude_Lower = float(Min_Magnitude_Lower)
    # Check if Min_Magnitude_Upper is null
    Min_Magnitude_Upper = request.form['Min_Magnitude_Upper']
    if Min_Magnitude_Upper == "":     # it was blank to begin with
        Min_Magnitude_Upper = None
    else:
        Min_Magnitude_Upper = float(Min_Magnitude_Upper)
    # Check that Min_Magnitude_Upper is greater than Min_Magnitude_Lower
    if (Min_Magnitude_Lower != None) and (Min_Magnitude_Upper != None):
        if Min_Magnitude_Lower > Min_Magnitude_Upper: return redirect("localhost:5000/index.html")

    # Maximum Variable Magnitude
    # Check if Max_Magnitude_Lower is null
    Max_Magnitude_Lower = request.form['Max_Magnitude_Lower']
    if Max_Magnitude_Lower == "":     # it was blank to begin with
        Max_Magnitude_Lower = None
    else:
        Max_Magnitude_Lower = float(Max_Magnitude_Lower)
    # Check if Max_Magnitude_Upper is null
    Max_Magnitude_Upper = request.form['Max_Magnitude_Upper']
    if Max_Magnitude_Upper == "":     # it was blank to begin with
        Max_Magnitude_Upper = None
    else:
        Max_Magnitude_Upper = float(Max_Magnitude_Upper)
    # Check that Max_Magnitude_Upper is greater than Max_Magnitude_Lower
    if (Max_Magnitude_Lower != None) and (Max_Magnitude_Upper != None):
        if Max_Magnitude_Lower > Max_Magnitude_Upper: return redirect("localhost:5000/index.html")

    # Check if CompanionID is null
    try:
        CompanionID = int(request.form['CompanionID'])
    except:
        CompanionID = None  # it was blank to begin with

    # Put everything together into a dictionary that represents everything the user input.
    criteria = {"HipparcosID": HipparcosID,
                "Constellation": Constellation,
                "Spectral Type": SpectralType,
                "Distance Lower": Distance_Lower, "Distance Upper": Distance_Upper,
                "RA Lower": RA_Lower, "RA Upper": RA_Upper,
                "Dec Lower": Dec_Lower, "Dec Upper": Dec_Upper,
                "Magnitude Lower": Magnitude_Lower, "Magnitude Upper": Magnitude_Upper,
                "Absolute Magnitude Lower": Absolute_Magnitude_Lower, "Absolute Magnitude Upper": Absolute_Magnitude_Upper,
                "Luminosity Lower": Luminosity_Lower, "Luminosity Upper": Luminosity_Upper,
                "Min Magnitude Lower": Min_Magnitude_Lower, "Min Magnitude Upper": Min_Magnitude_Upper,
                "Max Magnitude Lower": Max_Magnitude_Lower, "Max Magnitude Upper": Max_Magnitude_Upper,
                "Companions": CompanionID}

    # Query the database using the information from the dictionary
    query= NovaBackend.ParseQuery(criteria)
    # It's important to limit the distance because when distance = 100000 it throws the entire scale off
    query += ("AND Distance <= 50000; ")
    print(query)
    # Query the database
    results= NovaBackend.NovaQuery(query)
    # Direct the results to the appropriate webpage based on the number of stars returned.
    if len(results["HipparcosID"]) == 0:
        print("No search results")
        return redirect("localhost:5000/index.html")    # There were no search results
    elif len(results["HipparcosID"]) == 1:
        print("Only 1 search result")
        return redirect("localhost:5000/single_star.html")  # Go to the single star results page
    elif len(results["HipparcosID"]) == 2:
        print("Multiple search results")
        return redirect("localhost:5000/comparison.html")  # Go to the comparison results page
    else:
        # Generate a 3D scatterplot of the results and display it on the multistar results page
        NovaBackend.MultiStarPlot(results)
        #return redirect("localhost:5000/multistar.html")

    return redirect("localhost:5000/index.html")

## Starts the server for serving Rest Services
if __name__ == '__main__':
    app.run(debug=False)
