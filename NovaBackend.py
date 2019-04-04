import mysql.connector                   # This will connect us to MySQL Workbench
from mysql.connector import errorcode    # This will catch some errors that might arise when connecting
#import matplotlib.pyplot as plt          # We'll generate the plot with matplotlib
import numpy as np                       # Standard math and array library
import pandas as pd                      # Standard dataframe library
#import plotly
#import plotly.graph_objs as go
#import numpy as np
#from matplotlib.pyplot import figure
#import mpld3
import matplotlib.pyplot as plt
from matplotlib.pyplot import mpld3

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
    conn = mysql.connector.connect(user='root', password='Mg24682468', host='localhost', database='novadb')
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
                if k >= 0:
					ax.plot([i,i],[j,j],[0,k],color = 'b', alpha= .3)
                else:
					ax.plot([i,i],[j,j],[0,k], color = 'r', alpha= .3)
    ax.set_facecolor('black')
    ax.grid(False)
    ax.set_axis_off()
    ax.imshow(wordcloud)
	plt.show()
#	d3plot = mpld3.fig_to_html(fig, template_type="simple")
#	print(d3plot)

#	mpld3.save_html(fig,"test.html")
#	mpld3.fig_to_html(fig,template_type="simple")
#	mpld3.disable_notebook()
#	mpld3.show()
#	html1 = mpld3.fig_to_html(fig)
#	html_graph = mpld3.fig_to_html(fig)
	
	
