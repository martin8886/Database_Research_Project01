USE NovaDB;
-- When loading in the data, make sure 'local_infile' is set to on.  Check with the following command:
SHOW VARIABLES LIKE 'local_infile';
-- If it is off, change it to on with the following command.
-- SET GLOBAL local_infile = 1;
-- Next, the hygClean.csv must be saved into the directory given by the following command:
SHOW VARIABLES LIKE 'secure_file_priv';
-- This gives a file path.  Move the hygClean.csv to that path.

-- Often times when creating the hygClean table for the import, I'd get it wrong and have to drop it, then re-create differently.
-- drop table `hygClean`;

-- Create a table to hold all of the data from hygClean.csv
CREATE TABLE IF NOT EXISTS `hygClean` (
`Empty` INT NOT NULL,
`ID` INT NOT NULL,
`HipparcosID` INT NOT NULL,
`HenryDraperID` INT NULL,
`HarvardRevisedID` INT NULL,
`GlieseID` VARCHAR(20) NULL,
`BayerFlamsteed` VARCHAR(20) NULL,
`ProperName` VARCHAR(30) NULL,
`RA` VARCHAR(20) NULL,
`Dec` VARCHAR(20) NULL,
`Distance` FLOAT NULL,
`ProperMotion(RA)` VARCHAR(20) NULL,
`ProperMotion(Dec)` VARCHAR(20) NULL,
`RadialVelocity` FLOAT NULL,
`Magnitude` FLOAT NULL,
`AbsoluteMagnitude` FLOAT NULL,
`SpectralType` VARCHAR(20) NULL,
`ColorIndex` VARCHAR(20) NULL,
`X` VARCHAR(20) NULL,
`Y` VARCHAR(20) NULL,
`Z` VARCHAR(20) NULL,
`Vx` VARCHAR(20) NULL,
`Vy` VARCHAR(20) NULL,
`Vz` VARCHAR(20) NULL,
`RA(radians)` VARCHAR(20) NULL,
`Dec(radians)` VARCHAR(20) NULL,
`ProperMotionRA(radians)` VARCHAR(20) NULL,
`ProperMotionDec(radians)` VARCHAR(20) NULL,
`BayerDesignation` VARCHAR(20) NULL,
`FlamsteedNumber` INT NULL,
`Constellation` VARCHAR(20) NULL,
`CompanionID` INT NULL,
`PrimaryCompanionID` INT NULL,
`BaseName` VARCHAR(20) NULL,
`Luminosity` FLOAT NULL,
`VariableStarID` VARCHAR(20) NULL,
`VariableMinMagnitude` FLOAT NULL,
`VariableMaxMagnitude` FLOAT NULL,
PRIMARY KEY (`HipparcosID`));

-- Read in hygClean to the newly created table
SET sql_mode = "";  -- This allows various values (like INTs) to be blank rather than null.
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/hygClean.csv'
INTO TABLE `hygClean`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Make a test query to see if the data loaded in properly
SELECT Distance
FROM hygclean
where hipparcosID = 1;


-- This table will contain all the attribues we might want to display for a given star(s)
CREATE TABLE IF NOT EXISTS `Star` (
`HipparcosID` INT NOT NULL,
`HenryDraperID` INT,
`HarvardRevisedID` INT,
`GlieseID` INT,
`BayerFlamsteed` VARCHAR(20),
`ProperName` VARCHAR(30),
`RightAscension` DECIMAL,
`Declination` DECIMAL,
`Distance` FLOAT,
`Magnitude` FLOAT,
`AbsoluteMagnitude` FLOAT,
`SpectralType` VARCHAR(20),
`ColorIndex` FLOAT,
`ConstellationID` INT,
`Luminosity` FLOAT,
`CompanionID` INT,
`PrimaryCompanionID` INT,
`BaseName` VARCHAR(20),
`VariableStarID` VARCHAR(20),
`VariableMinMagnitude` FLOAT,
`VariableMaxMagnitude` FLOAT,
PRIMARY KEY (`HipparcosID`));

-- This table will contain the constellation information to include coordinates
CREATE TABLE IF NOT EXISTS `Constellation` (
`ConstellationID` INT,
`ConstellationName` VARCHAR(20),
`RightAscension` DECIMAL,
`Declination` DECIMAL,
-- Convert RA to Longitude
--     Convert RA to decimal: hour + minute/60 + second/3600 = decimal value.
--     Multiply the decimal time by 15 degrees.
--     If > 180, subtract 360 and this gives degrees latitude West
--     If < 180, this gives degrees latitude East
-- Convert Dec to Latitude
--     If > 0, this gives the latitude N
--     If < 0, multiply by -1.  This gives latitude S
`Longitude` DECIMAL,
`Latitude` DECIMAL,
`Shape` GEOMETRY,
PRIMARY KEY (`ConstellationID`));

-- This table is where we relate stars to constellation.  Star X resides in Constellation Y
CREATE TABLE IF NOT EXISTS `Resides` (
`Star_HipparcosID` INT,
`Constellation_ConstellationID` INT);