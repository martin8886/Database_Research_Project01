CREATE DATABASE NovaDB;
USE NovaDB;

-- This table will contain all the attribues we might want to display for a given star(s)
CREATE TABLE Star
(
HipparcosID INT,
HenryDraperID INT,
HarvardRevisedID INT,
GlieseID INT,
BayerFlamsteed VARCHAR(20),
ProperName VARCHAR(30),
RightAscension DECIMAL,
Declination DECIMAL,
Distance FLOAT,
Magnitude FLOAT,
AbsoluteMagnitude FLOAT,
SpectralType VARCHAR(20),
ColorIndex FLOAT,
ConstellationID INT,
Luminosity FLOAT,
CompanionID INT,
PrimaryCompanionID INT,
BaseName VARCHAR(20),
VariableStarID VARCHAR(20),
VariableMinMagnitude FLOAT,
VariableMaxMagnitude FLOAT
);

-- This table will contain the constellation information to include coordinates
CREATE TABLE Constellation
(
ConstellationID INT,
ConstellationName VARCHAR(20),
RightAscension DECIMAL,
Declination DECIMAL,
-- Convert RA to Longitude
--     Convert RA to decimal: hour + minute/60 + second/3600 = decimal value.
--     Multiply the decimal time by 15 degrees.
--     If > 180, subtract 360 and this gives degrees latitude West
--     If < 180, this gives degrees latitude East
-- Convert Dec to Latitude
--     If > 0, this gives the latitude N
--     If < 0, multiply by -1.  This gives latitude S
Longitude DECIMAL,
Latitude DECIMAL,
Shape GEOMETRY
);

-- This table is where we relate stars to constellation.  Star X resides in Constellation Y
CREATE TABLE Resides
(
Star_HipparcosID INT,
Constellation_ConstellationID INT
);