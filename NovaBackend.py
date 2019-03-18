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
        query = ("SELECT * FROM Star WHERE HipparcosID = %i; " %results["HipparcosID"])
    # otherwise it's probably a multistar search
    else:
        # in which case, we'll probably want to piece together the query
        query_WHERE = None
        # Starting with Constellation,
        if results["Constellation"] != None:
            query_WHERE = "WHERE Constellation = '%s' " %results["Constellation"]
        if results["Spectral Type"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE SpectralType = '%s' " %results["Spectral Type"]
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND SpectralType = '%s' " %results["Spectral Type"]
        # Remember, we need ALL 3 fields or the decimal RA to be present here to work
        if results["RA Hours"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE RA = '%s' " % str(results["RA Hours"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND RA = '%s' " % str(results["RA Hours"])
        if results["Dec"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE Dec = '%s' " % str(results["Dec"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND Dec = '%s' " % str(results["Dec"])
        # When checking distance, we'll need to adjust this to accept a range of distances.  That is,
        # from distance1 to distance2.
        if results["Distance"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE Distance = '%s' " % str(results["Distance"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND Distance = '%s' " % str(results["Distance"])
        # Likewise with Magnitude, Absolute Magnitude, and Luminosity.  Ranges are approprite
        if results["Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE Magnitude = '%s' " % str(results["Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND Magnitude = '%s' " % str(results["Magnitude"])
        if results["Absolute Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE AbsoluteMagnitude = '%s' " % str(results["Absolute Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND AbsoluteMagnitude = '%s' " % str(results["Absolute Magnitude"])
        if results["Luminosity"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE Luminosity = '%s' " % str(results["Luminosity"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND Luminosity = '%s' " % str(results["Luminosity"])
        if results["Min Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE VariableMinMagnitude = '%s' " % str(results["Min Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND VariableMinMagnitude = '%s' " % str(results["Min Magnitude"])
        if results["Max Magnitude"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE VariableMaxMagnitude = '%s' " % str(results["Max Magnitude"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND VariableMaxMagnitude = '%s' " % str(results["Max Magnitude"])
        # Star System Name will probably require some prior knowledge since these are not intuitive.
        # Maybe we could somehow incororate a mechanism that checks if the spelling is 'close enough'
        if results["Star System Name"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE BaseName = '%s' " % str(results["Star System Name"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND BaseName = '%s' " % str(results["Star System Name"])
        # Last one is either 1, 2, or 3 if not null.
        if results["Companions"] != None:
            # Check if there's an existing WHERE clause
            if query_WHERE == None:
                query_WHERE = "WHERE CompanionID = '%s' " % str(results["Companions"])
            else:
                # If so, append to it with the AND statement
                query_WHERE += " AND CompanionID = '%s' " % str(results["Companions"])
        query = ("SELECT * FROM Star " + query_WHERE + "; ")
    return(query)
