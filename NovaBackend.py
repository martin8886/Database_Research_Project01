import mysql.connector                   # This will connect us to MySQL Workbench
from mysql.connector import errorcode    # This will catch some errors that might arise when connecting
import matplotlib.pyplot as plt          # We'll generate the plot with matplotlib
import mpld3
import numpy as np                       # Standard math and array library
import pandas as pd                      # Standard dataframe library

def ParseQuery(criteria):
    '''This function will analyze which fields have been entered and then construct a string to be used
    in a MySQL query to generate search results.'''
    # First determine if we're querying 1 star, many stars, or a constellation.
    if criteria["HipparcosID"] != None:
        # This means the user has entered a specific HipparcosID.  We'll want to query that specific star
        query = ("SELECT * FROM Star WHERE `HipparcosID` = {}; ".format(criteria["HipparcosID"]))
    # otherwise it's probably a multistar search
    else:
        # in which case, we'll probably want to piece together the query
        query_WHERE = None
        # Starting with Constellation,
        if criteria["Constellation"] != None:
            query_WHERE = "WHERE `ConstellationID` = '{}' ".format(criteria["Constellation"])
        # Spectral Type
        if criteria["Spectral Type"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE LEFT(`SpectralType`, 1) = '{}' ".format(criteria["Spectral Type"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND LEFT(`SpectralType`, 1) = '{}' ".format(criteria["Spectral Type"])
        # Distance
        if criteria["Distance Lower"] != None:      # This works because Lower and Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Distance` >= {} AND `Distance` <= {} ".format(str(criteria["Distance Lower"]), str(criteria["Distance Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `Distance` >= {} AND `Distance` <= {} ".format(str(criteria["Distance Lower"]), str(criteria["Distance Upper"]))
        # RA
        if criteria["RA Lower"] != None:     # This works because RA Lower and RA Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `RA` >= '{}' AND `RA` <= '{}' ".format(str(criteria["RA Lower"]), str(criteria["RA Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `RA` >= '{}' AND `RA` <= '{}' ".format(str(criteria["RA Lower"]), str(criteria["RA Upper"]))
        # Dec
        if criteria["Dec Lower"] != None:     # This works because Dec Lower and Dec Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Dec` >= '{}' AND `Dec` <= '{}' ".format(str(criteria["Dec Lower"]), str(criteria["Dec Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `Dec` >= '{}' AND `Dec` <= '{}' ".format(str(criteria["Dec Lower"]), str(criteria["Dec Upper"]))
        # Magnitude
        if criteria["Magnitude Lower"] != None:     # This works because Lower and Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Magnitude` >= '{}' AND `Magnitude` <= '{}' ".format(str(criteria["Magnitude Lower"]), str(criteria["Magnitude Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `Magnitude` >= '{}' AND `Magnitude` <= '{}' ".format(str(criteria["Magnitude Lower"]), str(criteria["Magnitude Upper"]))
        # Absolute Magnitude
        if criteria["Absolute Magnitude Lower"] != None:     # This works because Lower and Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `AbsoluteMagnitude` >= '{}' AND `AbsoluteMagnitude` <= '{}' ".format(str(criteria["Absolute Magnitude Lower"]), str(criteria["Absolute Magnitude Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `AbsoluteMagnitude` >= '{}' AND `AbsoluteMagnitude` <= '{}' ".format(str(criteria["Absolute Magnitude Lower"]), str(criteria["Absolute Magnitude Upper"]))
        # Luminosity
        if criteria["Luminosity Lower"] != None:     # This works because Lower and Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Luminosity` >= '{}' AND `Luminosity` <= '{}' ".format(str(criteria["Luminosity Lower"]), str(criteria["Luminosity Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `Luminosity` >= '{}' AND `Luminosity` <= '{}' ".format(str(criteria["Luminosity Lower"]), str(criteria["Luminosity Upper"]))
        # Minimum Variable Magnitude
        if criteria["Min Magnitude Lower"] != None:     # This works because Lower and Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `VariableMinMagnitude` >= '{}' AND `VariableMinMagnitude` <= '{}' ".format(str(criteria["Min Magnitude Lower"]), str(criteria["Min Magnitude Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `VariableMinMagnitude` >= '{}' AND `VariableMinMagnitude` <= '{}' ".format(str(criteria["Min Magnitude Lower"]), str(criteria["Min Magnitude Upper"]))
        # Maximum Variable Magnitude
        if criteria["Max Magnitude Lower"] != None:     # This works because Lower and Upper have to be present to work
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `VariableMaxMagnitude` >= '{}' AND `VariableMaxMagnitude` <= '{}' ".format(str(criteria["Max Magnitude Lower"]), str(criteria["Max Magnitude Upper"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += "AND `VariableMaxMagnitude` >= '{}' AND `VariableMaxMagnitude` <= '{}' ".format(str(criteria["Max Magnitude Lower"]), str(criteria["Max Magnitude Upper"]))
        # Companions
        if criteria["Companions"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `CompanionID` = {} ".format(str(criteria["Companions"]))
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `CompanionID` = {} ".format(str(criteria["Companions"]))
        query = ("SELECT * FROM Star " + query_WHERE)
    return(query)

# Fetch the results of the query and store it in a pandas dataframe.
def NovaQuery(query):
    conn = mysql.connector.connect(user='root', password='Drew$kiWi1kins09!', host='127.0.0.1', database='NovaDB')
    cursor = conn.cursor()
    cursor.execute(query)
    results = pd.DataFrame(cursor.fetchall(), columns= ["HipparcosID", "HenryDraperID", "HarvardRevisedID", "GlieseID",
        "BayerFlamsteed", "ProperName", "RA", "Dec", "Distance", "Magnitude", "AbsoluteMagnitude", "SpectralType",
        "ColorIndex", "X", "Y", "Z", "RA(radians)", "Dec(radians)", "ConstellationID", "Luminosity", "CompanionID",
        "PrimaryCompanionID", "BaseName", "VariableStarID", "VariableMinMagnitude", "VariableMaxMagnitude"])
    cursor.close()
    conn.close()
    return(results)

# Get the attribtes of each star in the results based on spectral type for the 3D plot
def StarType(spectraltype):
    # Define a few empty lists (or arrays)
    startype = list(spectraltype)   # This holds the letter of the spectral type: O B A F G K M C or U for Unknown
    starsize = np.zeros(len(spectraltype))  # This will determine the size of the star on the plot
    starcolor = ["" for star in range(0, len(spectraltype))]  # Determines color on the plot
    # Go through every search result and assign the relevant attributes
    for i in range(0, len(spectraltype)):
        # Try to grab the first letter of spectral type
        try:
            startype[i] = spectraltype[i][0]
        except:
        # If it didn't work, it's because the value was null, so we assign it "U" for "Unknown"
            startype[i] = "U"
        # Then, depending on the spectral type, assign some meaningful sizes and colors
        if startype[i] == "O":
            starsize[i] = 4
            starcolor[i] = "blue"
        elif startype[i] == "B":
            starsize[i] = 3.5
            starcolor[i] = "darkturquoise"
        elif startype[i] == "A":
            starsize[i] = 3
            starcolor[i] = "paleturquoise"
        elif startype[i] == "F":
            starsize[i] = 2.5
            starcolor[i] = "white"
        elif startype[i] == "G":
            starsize[i] = 2
            starcolor[i] = "yellow"
        elif startype[i] == "K":
            starsize[i] = 1.5
            starcolor[i] = "orange"
        elif startype[i] == "M":
            starsize[i] = 1
            starcolor[i] = "red"
        elif startype[i] == "C":
            starsize[i] = 3
            starcolor[i] = "maroon"
        else:
            starsize[i] = 2
            starcolor[i] = "gold"
    return(startype, starsize, starcolor)

# Generate a 3D scatterplot of the results
def MultiStarPlot(results):
    # Get the attributes for each star on the 3D plot
    startype, starsize, starcolor = StarType(results["SpectralType"])

    # Code up the plot
    from mpl_toolkits.mplot3d import Axes3D
    # Define the 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Read the data from the query as a list
    xs = list(pd.to_numeric(results["X"]))
    ys = list(pd.to_numeric(results["Y"]))
    zs = list(pd.to_numeric(results["Z"]))
    # Draw the scatterplot using the colors and sizes we determined above
    ax.scatter(xs, ys, zs, c= starcolor, s= starsize, depthshade= False)
    # The axis wont be centered initially, so let's fix that.  Start by getting the max value on each dimension
    xlim = max(np.abs(ax.get_xlim()))
    ylim = max(np.abs(ax.get_ylim()))
    zlim = max(np.abs(ax.get_zlim()))
    # Then set the axis on each dimension such that 0 is in the middle of the max value
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.set_zlim(-zlim, zlim)
    # Draw a plane at z= 0.  This is purely for asthetics so you can get a sense of each star's location
    xx, yy = np.meshgrid(np.arange(-xlim, xlim, 5), np.arange(-ylim, ylim, 5))
    z = xx * 0
    ax.plot_wireframe(xx, yy, z, alpha=0.5, rcount= 5, ccount= 5, colors= "w")
    # Draw lines from the z=0 plane to the star if there's only a few stars.  Otherwise this takes WAY too long.
    if len(xs) < 1000:
        for i,j,k in zip(xs, ys, zs):
            if (i != 0) and (j != 0) and (k != 0):
                if k >= 0: ax.plot([i,i],[j,j],[0,k],color = 'b', alpha= .3)
                else: ax.plot([i,i],[j,j],[0,k], color = 'r', alpha= .3)
    ax.set_facecolor('black')
    ax.grid(False)
    ax.set_axis_off()
    return(fig)
    #plt.show()

# This is another function to grab the spectral type to identify which picture to use.
# This one only works for dictionarys
def StarPic(results):
    # Add a special case just for the sun.
    if results["HipparcosID"] == 0:
        StarPicture = "Sun Resized.jpg"
        ConstellationPicture = "Question Resized.jpg"
    elif results["SpectralType"][0][0] == "O":
        StarPicture = "O Class Star Resized.png"
    elif results["SpectralType"][0][0] == "B":
        StarPicture = "B Class Star Resized.png"
    elif results["SpectralType"][0][0] == "A":
        StarPicture = "A Class Star Resized.png"
    elif results["SpectralType"][0][0] == "F":
        StarPicture = "F Class Star Resized.png"
    elif results["SpectralType"][0][0] == "G":
        StarPicture = "G Class Star Resized.png"
    elif results["SpectralType"][0][0] == "K":
        StarPicture = "K Class Star Resized.png"
    elif results["SpectralType"][0][0] == "M":
        StarPicture = "M Class Star Resized.png"
    elif results["SpectralType"][0][0] == "C":
        StarPicture = "C Class Star Resized.png"
    else:
        StarPicture = "Question Resized.jpg"
    # Now figure out which constellation picture to use.
    if results["ConstellationID"] == "And": ConstellationPicture = "/ConstellationPictures/AND.gif"
    elif results["ConstellationID"] == "Ant": ConstellationPicture = "/ConstellationPictures/ANT.gif"
    elif results["ConstellationID"] == "Aps": ConstellationPicture = "/ConstellationPictures/APS.gif"
    elif results["ConstellationID"] == "Aql": ConstellationPicture = "/ConstellationPictures/AQL.gif"
    elif results["ConstellationID"] == "Aqr": ConstellationPicture = "/ConstellationPictures/AQR.gif"
    elif results["ConstellationID"] == "Ara": ConstellationPicture = "/ConstellationPictures/ARA.gif"
    elif results["ConstellationID"] == "Ari": ConstellationPicture = "/ConstellationPictures/ARI.gif"
    elif results["ConstellationID"] == "Aur": ConstellationPicture = "/ConstellationPictures/AUR.gif"
    elif results["ConstellationID"] == "Boo": ConstellationPicture = "/ConstellationPictures/BOO.gif"
    elif results["ConstellationID"] == "Cae": ConstellationPicture = "/ConstellationPictures/CAE.gif"
    elif results["ConstellationID"] == "Cam": ConstellationPicture = "/ConstellationPictures/CAM.gif"
    elif results["ConstellationID"] == "Cap": ConstellationPicture = "/ConstellationPictures/CAP.gif"
    elif results["ConstellationID"] == "Car": ConstellationPicture = "/ConstellationPictures/CAR.gif"
    elif results["ConstellationID"] == "Cas": ConstellationPicture = "/ConstellationPictures/CAS.gif"
    elif results["ConstellationID"] == "Cen": ConstellationPicture = "/ConstellationPictures/CEN.gif"
    elif results["ConstellationID"] == "Cep": ConstellationPicture = "/ConstellationPictures/CEP.gif"
    elif results["ConstellationID"] == "Cet": ConstellationPicture = "/ConstellationPictures/CET.gif"
    elif results["ConstellationID"] == "Cha": ConstellationPicture = "/ConstellationPictures/CHA.gif"
    elif results["ConstellationID"] == "Cir": ConstellationPicture = "/ConstellationPictures/CIR.gif"
    elif results["ConstellationID"] == "Cma": ConstellationPicture = "/ConstellationPictures/CMA.gif"
    elif results["ConstellationID"] == "Cmi": ConstellationPicture = "/ConstellationPictures/CMI.gif"
    elif results["ConstellationID"] == "Cnc": ConstellationPicture = "/ConstellationPictures/CNC.gif"
    elif results["ConstellationID"] == "Col": ConstellationPicture = "/ConstellationPictures/COL.gif"
    elif results["ConstellationID"] == "Com": ConstellationPicture = "/ConstellationPictures/COM.gif"
    elif results["ConstellationID"] == "Cra": ConstellationPicture = "/ConstellationPictures/CRA.gif"
    elif results["ConstellationID"] == "Crb": ConstellationPicture = "/ConstellationPictures/CRB.gif"
    elif results["ConstellationID"] == "Crt": ConstellationPicture = "/ConstellationPictures/CRT.gif"
    elif results["ConstellationID"] == "Cru": ConstellationPicture = "/ConstellationPictures/CRU.gif"
    elif results["ConstellationID"] == "Crv": ConstellationPicture = "/ConstellationPictures/CRV.gif"
    elif results["ConstellationID"] == "Cvn": ConstellationPicture = "/ConstellationPictures/CVN.gif"
    elif results["ConstellationID"] == "Cyg": ConstellationPicture = "/ConstellationPictures/CYG.gif"
    elif results["ConstellationID"] == "Del": ConstellationPicture = "/ConstellationPictures/DEL.gif"
    elif results["ConstellationID"] == "Dor": ConstellationPicture = "/ConstellationPictures/DOR.gif"
    elif results["ConstellationID"] == "Dra": ConstellationPicture = "/ConstellationPictures/DRA.gif"
    elif results["ConstellationID"] == "Equ": ConstellationPicture = "/ConstellationPictures/EQU.gif"
    elif results["ConstellationID"] == "Eri": ConstellationPicture = "/ConstellationPictures/ERI.gif"
    elif results["ConstellationID"] == "For": ConstellationPicture = "/ConstellationPictures/FOR.gif"
    elif results["ConstellationID"] == "Gem": ConstellationPicture = "/ConstellationPictures/GEM.gif"
    elif results["ConstellationID"] == "Gru": ConstellationPicture = "/ConstellationPictures/GRU.gif"
    elif results["ConstellationID"] == "Her": ConstellationPicture = "/ConstellationPictures/HER.gif"
    elif results["ConstellationID"] == "Hor": ConstellationPicture = "/ConstellationPictures/HOR.gif"
    elif results["ConstellationID"] == "Hya": ConstellationPicture = "/ConstellationPictures/Hya.gif"
    elif results["ConstellationID"] == "Hyi": ConstellationPicture = "/ConstellationPictures/HYI.gif"
    elif results["ConstellationID"] == "Ind": ConstellationPicture = "/ConstellationPictures/IND.gif"
    elif results["ConstellationID"] == "Lac": ConstellationPicture = "/ConstellationPictures/LAC.gif"
    elif results["ConstellationID"] == "Leo": ConstellationPicture = "/ConstellationPictures/LEO.gif"
    elif results["ConstellationID"] == "Lep": ConstellationPicture = "/ConstellationPictures/LEP.gif"
    elif results["ConstellationID"] == "Lib": ConstellationPicture = "/ConstellationPictures/LIB.gif"
    elif results["ConstellationID"] == "Lmi": ConstellationPicture = "/ConstellationPictures/LMI.gif"
    elif results["ConstellationID"] == "Lup": ConstellationPicture = "/ConstellationPictures/LUP.gif"
    elif results["ConstellationID"] == "Lyn": ConstellationPicture = "/ConstellationPictures/LYN.gif"
    elif results["ConstellationID"] == "Lyr": ConstellationPicture = "/ConstellationPictures/LYR.gif"
    elif results["ConstellationID"] == "Men": ConstellationPicture = "/ConstellationPictures/MEN.gif"
    elif results["ConstellationID"] == "Mic": ConstellationPicture = "/ConstellationPictures/MIC.gif"
    elif results["ConstellationID"] == "Mon": ConstellationPicture = "/ConstellationPictures/MON.gif"
    elif results["ConstellationID"] == "Mus": ConstellationPicture = "/ConstellationPictures/MUS.gif"
    elif results["ConstellationID"] == "Nor": ConstellationPicture = "/ConstellationPictures/NOR.gif"
    elif results["ConstellationID"] == "Oct": ConstellationPicture = "/ConstellationPictures/OCT.gif"
    elif results["ConstellationID"] == "Oph": ConstellationPicture = "/ConstellationPictures/Oph.gif"
    elif results["ConstellationID"] == "Ori": ConstellationPicture = "/ConstellationPictures/ORI.gif"
    elif results["ConstellationID"] == "Pav": ConstellationPicture = "/ConstellationPictures/PAV.gif"
    elif results["ConstellationID"] == "Peg": ConstellationPicture = "/ConstellationPictures/PEG.gif"
    elif results["ConstellationID"] == "Per": ConstellationPicture = "/ConstellationPictures/PER.gif"
    elif results["ConstellationID"] == "Phe": ConstellationPicture = "/ConstellationPictures/PHE.gif"
    elif results["ConstellationID"] == "Pic": ConstellationPicture = "/ConstellationPictures/PIC.gif"
    elif results["ConstellationID"] == "Psa": ConstellationPicture = "/ConstellationPictures/PSA.gif"
    elif results["ConstellationID"] == "Psc": ConstellationPicture = "/ConstellationPictures/PSC.gif"
    elif results["ConstellationID"] == "Pup": ConstellationPicture = "/ConstellationPictures/PUP.gif"
    elif results["ConstellationID"] == "Pyx": ConstellationPicture = "/ConstellationPictures/PYX.gif"
    elif results["ConstellationID"] == "Ret": ConstellationPicture = "/ConstellationPictures/RET.gif"
    elif results["ConstellationID"] == "Scl": ConstellationPicture = "/ConstellationPictures/SCL.gif"
    elif results["ConstellationID"] == "Sco": ConstellationPicture = "/ConstellationPictures/SCO.gif"
    elif results["ConstellationID"] == "Sct": ConstellationPicture = "/ConstellationPictures/SCT.gif"
    elif results["ConstellationID"] == "Ser1": ConstellationPicture = "/ConstellationPictures/SER1.gif"
    elif results["ConstellationID"] == "Ser2": ConstellationPicture = "/ConstellationPictures/SER2.gif"
    elif results["ConstellationID"] == "Sex": ConstellationPicture = "/ConstellationPictures/SEX.gif"
    elif results["ConstellationID"] == "Sge": ConstellationPicture = "/ConstellationPictures/SGE.gif"
    elif results["ConstellationID"] == "Sgr": ConstellationPicture = "/ConstellationPictures/SGR.gif"
    elif results["ConstellationID"] == "Tau": ConstellationPicture = "/ConstellationPictures/TAU.gif"
    elif results["ConstellationID"] == "Tel": ConstellationPicture = "/ConstellationPictures/TEL.gif"
    elif results["ConstellationID"] == "Tra": ConstellationPicture = "/ConstellationPictures/TRA.gif"
    elif results["ConstellationID"] == "Tri": ConstellationPicture = "/ConstellationPictures/TRI.gif"
    elif results["ConstellationID"] == "Tuc": ConstellationPicture = "/ConstellationPictures/TUC.gif"
    elif results["ConstellationID"] == "Uma": ConstellationPicture = "/ConstellationPictures/UMA.gif"
    elif results["ConstellationID"] == "Umi": ConstellationPicture = "/ConstellationPictures/UMI.gif"
    elif results["ConstellationID"] == "Vel": ConstellationPicture = "/ConstellationPictures/VEL.gif"
    elif results["ConstellationID"] == "Vir": ConstellationPicture = "/ConstellationPictures/VIR.gif"
    elif results["ConstellationID"] == "Vol": ConstellationPicture = "/ConstellationPictures/VOL.gif"
    elif results["ConstellationID"] == "Vul": ConstellationPicture = "/ConstellationPictures/VUL.gif"
    else: ConstellationPicture = "Question Resized.jpg"
    return(StarPicture, ConstellationPicture)

# This function will return the full constellation name.
def ConstellationName(results):
    if results["ConstellationID"] == "And": ConstellationName = "Andromeda"
    elif results["ConstellationID"] == "Ant": ConstellationName = "Antlia"
    elif results["ConstellationID"] == "Aps": ConstellationName = "Apus"
    elif results["ConstellationID"] == "Aql": ConstellationName = "Aquila"
    elif results["ConstellationID"] == "Aqr": ConstellationName = "Aquarius"
    elif results["ConstellationID"] == "Ara": ConstellationName = "Ara"
    elif results["ConstellationID"] == "Ari": ConstellationName = "Aries"
    elif results["ConstellationID"] == "Aur": ConstellationName = "Auriga"
    elif results["ConstellationID"] == "Boo": ConstellationName = "Bootes"
    elif results["ConstellationID"] == "Cae": ConstellationName = "Caelum"
    elif results["ConstellationID"] == "Cam": ConstellationName = "Camelopardalis"
    elif results["ConstellationID"] == "Cap": ConstellationName = "Capricornus"
    elif results["ConstellationID"] == "Car": ConstellationName = "Carina"
    elif results["ConstellationID"] == "Cas": ConstellationName = "Cassiopeia"
    elif results["ConstellationID"] == "Cen": ConstellationName = "Centaurus"
    elif results["ConstellationID"] == "Cep": ConstellationName = "Cepheus"
    elif results["ConstellationID"] == "Cet": ConstellationName = "Cetus"
    elif results["ConstellationID"] == "Cha": ConstellationName = "Chamaeleon"
    elif results["ConstellationID"] == "Cir": ConstellationName = "Circinus"
    elif results["ConstellationID"] == "Cma": ConstellationName = "Canis Major"
    elif results["ConstellationID"] == "Cmi": ConstellationName = "Canis Minor"
    elif results["ConstellationID"] == "Cnc": ConstellationName = "Cancer"
    elif results["ConstellationID"] == "Col": ConstellationName = "Columba"
    elif results["ConstellationID"] == "Com": ConstellationName = "Coma Berenicies"
    elif results["ConstellationID"] == "Cra": ConstellationName = "Corona Australis"
    elif results["ConstellationID"] == "Crb": ConstellationName = "Corona Borealis"
    elif results["ConstellationID"] == "Crt": ConstellationName = "Crater"
    elif results["ConstellationID"] == "Cru": ConstellationName = "Crux"
    elif results["ConstellationID"] == "Crv": ConstellationName = "Corvus"
    elif results["ConstellationID"] == "Cvn": ConstellationName = "Canes Venatici"
    elif results["ConstellationID"] == "Cyg": ConstellationName = "Cygnus"
    elif results["ConstellationID"] == "Del": ConstellationName = "Delphinus"
    elif results["ConstellationID"] == "Dor": ConstellationName = "Dorado"
    elif results["ConstellationID"] == "Dra": ConstellationName = "Draco"
    elif results["ConstellationID"] == "Equ": ConstellationName = "Equuleus"
    elif results["ConstellationID"] == "Eri": ConstellationName = "Eridanus"
    elif results["ConstellationID"] == "For": ConstellationName = "Fornax"
    elif results["ConstellationID"] == "Gem": ConstellationName = "Gemini"
    elif results["ConstellationID"] == "Gru": ConstellationName = "Grus"
    elif results["ConstellationID"] == "Her": ConstellationName = "Hercules"
    elif results["ConstellationID"] == "Hor": ConstellationName = "Horologium"
    elif results["ConstellationID"] == "Hya": ConstellationName = "Hydra"
    elif results["ConstellationID"] == "Hyi": ConstellationName = "Hydrus"
    elif results["ConstellationID"] == "Ind": ConstellationName = "Indus"
    elif results["ConstellationID"] == "Lac": ConstellationName = "Lacerta"
    elif results["ConstellationID"] == "Leo": ConstellationName = "Leo"
    elif results["ConstellationID"] == "Lep": ConstellationName = "Lepus"
    elif results["ConstellationID"] == "Lib": ConstellationName = "Libra"
    elif results["ConstellationID"] == "Lmi": ConstellationName = "Leo Minor"
    elif results["ConstellationID"] == "Lup": ConstellationName = "Lupus"
    elif results["ConstellationID"] == "Lyn": ConstellationName = "Lynx"
    elif results["ConstellationID"] == "Lyr": ConstellationName = "Lyra"
    elif results["ConstellationID"] == "Men": ConstellationName = "Mensa"
    elif results["ConstellationID"] == "Mic": ConstellationName = "Microscopium"
    elif results["ConstellationID"] == "Mon": ConstellationName = "Monoceros"
    elif results["ConstellationID"] == "Mus": ConstellationName = "Musca"
    elif results["ConstellationID"] == "Nor": ConstellationName = "Norma"
    elif results["ConstellationID"] == "Oct": ConstellationName = "Octans"
    elif results["ConstellationID"] == "Oph": ConstellationName = "Ophiuchus"
    elif results["ConstellationID"] == "Ori": ConstellationName = "Ori on"
    elif results["ConstellationID"] == "Pav": ConstellationName = "/Pavo"
    elif results["ConstellationID"] == "Peg": ConstellationName = "Pegasus"
    elif results["ConstellationID"] == "Per": ConstellationName = "Perseus"
    elif results["ConstellationID"] == "Phe": ConstellationName = "Phoenix"
    elif results["ConstellationID"] == "Pic": ConstellationName = "Pictor"
    elif results["ConstellationID"] == "Psa": ConstellationName = "Piscis Austrinus"
    elif results["ConstellationID"] == "Psc": ConstellationName = "Pisces"
    elif results["ConstellationID"] == "Pup": ConstellationName = "Puppis"
    elif results["ConstellationID"] == "Pyx": ConstellationName = "Pyxis"
    elif results["ConstellationID"] == "Ret": ConstellationName = "Reticulum"
    elif results["ConstellationID"] == "Scl": ConstellationName = "Sculptor"
    elif results["ConstellationID"] == "Sco": ConstellationName = "Scorpius"
    elif results["ConstellationID"] == "Sct": ConstellationName = "Scutum"
    elif results["ConstellationID"] == "Ser1": ConstellationName = "Serpens Cauda"
    elif results["ConstellationID"] == "Ser2": ConstellationName = "Serpens Caput"
    elif results["ConstellationID"] == "Sex": ConstellationName = "Sextans"
    elif results["ConstellationID"] == "Sge": ConstellationName = "Sagitta"
    elif results["ConstellationID"] == "Sgr": ConstellationName = "Sagittarius"
    elif results["ConstellationID"] == "Tau": ConstellationName = "Taurus.gif"
    elif results["ConstellationID"] == "Tel": ConstellationName = "Telescopium"
    elif results["ConstellationID"] == "Tra": ConstellationName = "Triangulum Australe"
    elif results["ConstellationID"] == "Tri": ConstellationName = "Triangulum"
    elif results["ConstellationID"] == "Tuc": ConstellationName = "Tucana"
    elif results["ConstellationID"] == "Uma": ConstellationName = "Ursa Major"
    elif results["ConstellationID"] == "Umi": ConstellationName = "Ursa Minor"
    elif results["ConstellationID"] == "Vel": ConstellationName = "Vela"
    elif results["ConstellationID"] == "Vir": ConstellationName = "Virgo"
    elif results["ConstellationID"] == "Vol": ConstellationName = "Volans"
    elif results["ConstellationID"] == "Vul": ConstellationName = "Vulpecula"
    else: ConstellationName = "Unknown"
    return(ConstellationName)
