import mysql.connector                   # This will connect us to MySQL Workbench
from mysql.connector import errorcode    # This will catch some errors that might arise when connecting
import matplotlib.pyplot as plt          # We'll generate the plot with matplotlib
import numpy as np                       # Standard math and array library
import pandas as pd                      # Standard dataframe library

def ParseQuery(results):
    '''This function will analyze which fields have been entered and then construct a string to be used
    in a MySQL query to generate search results.'''
    # First determine if we're querying 1 star, many stars, or a constellation.
    if results["HipparcosID"] != None:
        # This means the user has entered a specific HipparcosID.  We'll want to query that specific star
        query = ("SELECT * FROM Star WHERE `HipparcosID` = %s; " %results["HipparcosID"])
    # otherwise it's probably a multistar search
    else:
        # in which case, we'll probably want to piece together the query
        query_WHERE = None
        # Starting with Constellation,
        if results["Constellation"] != None:
            query_WHERE = "WHERE `ConstellationID` = '%s' " %results["Constellation"]
        if results["Spectral Type"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE LEFT(`SpectralType`, 1) = '%s' " %results["Spectral Type"]
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND LEFT(`SpectralType`, 1) = '%s' " %results["Spectral Type"]
        # Remember, we need ALL 3 fields or the decimal RA to be present here to work
        if results["RA Hours"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `RA` = %s " % str(results["RA Hours"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `RA` = %s " % str(results["RA Hours"])
        if results["Dec"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Dec` = %s " % str(results["Dec"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `Dec` = %s " % str(results["Dec"])
        # When checking distance, we'll need to adjust this to accept a range of distances.  That is,
        # from distance1 to distance2.
        if results["Distance"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Distance` = %s " % str(results["Distance"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `Distance` = %s " % str(results["Distance"])
        # Likewise with Magnitude, Absolute Magnitude, and Luminosity.  Ranges are approprite
        if results["Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Magnitude` = %s " % str(results["Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `Magnitude` = %s " % str(results["Magnitude"])
        if results["Absolute Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `AbsoluteMagnitude` = %s " % str(results["Absolute Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `AbsoluteMagnitude` = %s " % str(results["Absolute Magnitude"])
        if results["Luminosity"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `Luminosity` = %s " % str(results["Luminosity"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `Luminosity` = %s " % str(results["Luminosity"])
        if results["Min Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `VariableMinMagnitude` = %s " % str(results["Min Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `VariableMinMagnitude` = %s " % str(results["Min Magnitude"])
        if results["Max Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `VariableMaxMagnitude` = %s " % str(results["Max Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `VariableMaxMagnitude` = %s " % str(results["Max Magnitude"])
        # Star System Name will probably require some prior knowledge since these are not intuitive.
        # Maybe we could somehow incororate a mechanism that checks if the spelling is 'close enough'
        if results["Star System Name"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `BaseName` = '%s' " % str(results["Star System Name"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `BaseName` = '%s' " % str(results["Star System Name"])
        # Last one is either 1, 2, or 3 if not null.
        if results["Companions"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE `CompanionID` = %s " % str(results["Companions"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND `CompanionID` = %s " % str(results["Companions"])
        query = ("SELECT * FROM Star " + query_WHERE)
    return(query)

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

def MultiStarPlot(query):
    conn = mysql.connector.connect(user='root', password='Drew$kiWi1kins09!', host='127.0.0.1', database='NovaDB')
    cursor = conn.cursor()

    # It's important to limit the distance because when distance = 100000 it throws the entire scale off
    query += (" AND Distance <= 50000; ")
    cursor.execute(query)
    result = pd.DataFrame(cursor.fetchall(), columns= ["HipparcosID", "HenryDraperID", "HarvardRevisedID", "GlieseID",
        "BayerFlamsteed", "ProperName", "RA", "Dec", "Distance", "Magnitude", "AbsoluteMagnitude", "SpectralType",
        "ColorIndex", "X", "Y", "Z", "RA(radians)", "Dec(radians)", "ConstellationID", "Luminosity", "CompanionID",
        "PrimaryCompanionID", "BaseName", "VariableStarID", "VariableMinMagnitude", "VariableMaxMagnitude"])
    cursor.close()
    conn.close()
    # Get the attributes for each star on the 3D plot
    startype, starsize, starcolor = StarType(result["SpectralType"])

    # Code up the plot
    from mpl_toolkits.mplot3d import Axes3D
    # Define the 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Read the data from the query as a list
    xs = list(pd.to_numeric(result["X"]))
    ys = list(pd.to_numeric(result["Y"]))
    zs = list(pd.to_numeric(result["Z"]))
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
    plt.show()
