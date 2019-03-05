USE novadb;
-- When loading in the data, make sure 'local_infile' is set to on.  Check with the following command:
SHOW VARIABLES LIKE 'local_infile';
-- If it is off, change it to on with the following command.
-- SET GLOBAL local_infile = 1;
-- Next, the hygClean.csv must be saved into the directory given by the following command:
SHOW VARIABLES LIKE 'secure_file_priv';
-- This gives a file path.  Move the hygClean.csv to that path.


-- Create a table to hold all of the data from hygClean.csv.
CREATE TABLE IF NOT EXISTS `hygClean` (
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


-- This table will contain all the attribues we might want to display for a given star(s).
CREATE TABLE IF NOT EXISTS `Star` (
`HipparcosID` INT NOT NULL,
`HenryDraperID` INT,
`HarvardRevisedID` INT,
`GlieseID` INT,
`BayerFlamsteed` VARCHAR(20),
`ProperName` VARCHAR(30),
`RA` DECIMAL(7,5),
`Dec` DECIMAL(7,5),
`Distance` FLOAT,
`Magnitude` FLOAT,
`AbsoluteMagnitude` FLOAT,
`SpectralType` VARCHAR(20),
`ColorIndex` FLOAT,
`ConstellationID` VARCHAR(20),
`Luminosity` FLOAT,
`CompanionID` INT,
`PrimaryCompanionID` INT,
`BaseName` VARCHAR(20),
`VariableStarID` VARCHAR(20),
`VariableMinMagnitude` FLOAT,
`VariableMaxMagnitude` FLOAT,
PRIMARY KEY (`HipparcosID`));


-- This table will contain the constellation information to including it's shape
CREATE TABLE IF NOT EXISTS `Constellation` (
`ConstellationID` VARCHAR(20),
`ConstellationName` VARCHAR(20),
`Shape` GEOMETRY,
PRIMARY KEY (`ConstellationID`));
UPDATE Constellation SET shape = ST_GeomFromText(ST_AsText(shape), 4326, 'axis-order=lat-long');


-- This table will have the coordinates in RA & Dec, and also Lat & Long that define the boundaries of each constellation.
CREATE TABLE IF NOT EXISTS `Boundaries` (
`BoundaryID` INT,
`ConstellationID` VARCHAR(20),
`RightAscension` DECIMAL(7,5),
`Declination` DECIMAL(7,5),
`Longitude` DECIMAL(8,5),
`Latitude` DECIMAL(7,5),
PRIMARY KEY (`BoundaryID`));
-- This table is populated using the import wizard (right click on the table in the Navigator under SCHEMAS and select
-- "Table Data Import Wizard" and select the "ConstellationCoordinate.csv."  The only tricky part here is that
-- ConstellationName is associated with ConstellationID and Index (or BoundaryID) is associated with BoundaryID.


-- This table is where we relate stars to constellation.  Star X resides in Constellation Y.
CREATE TABLE IF NOT EXISTS `Resides` (
`HipparcosID` INT,
`ConstellationID` VARCHAR(20));


-- Populate data into the Star table
INSERT INTO `Star` (`HipparcosID`, `HenryDraperID`, `HarvardRevisedID`, `GlieseID`, `BayerFlamsteed`, `ProperName`,
`RA`, `Dec`, `Distance`, `Magnitude`, `AbsoluteMagnitude`, `SpectralType`, `ColorIndex`,
`ConstellationID`, `Luminosity`, `CompanionID`, `PrimaryCompanionID`, `BaseName`, `VariableStarID`, `VariableMinMagnitude`,
`VariableMaxMagnitude`)  
SELECT `HipparcosID`, `HenryDraperID`, `HarvardRevisedID`, `GlieseID`, `BayerFlamsteed`, `ProperName`,
`RA`, `Dec`, `Distance`, `Magnitude`, `AbsoluteMagnitude`, `SpectralType`, `ColorIndex`,
`Constellation`, `Luminosity`, `CompanionID`, `PrimaryCompanionID`, `BaseName`, `VariableStarID`, `VariableMinMagnitude`,
`VariableMaxMagnitude`
FROM `hygClean`;


-- Convert RA to Longitude
--     Convert RA to decimal: hour + minute/60 + second/3600 = decimal value.  The data is already in decimal format.
--     Multiply the decimal time by 15 degrees.
--     If > 180, subtract 360 and this gives degrees latitude West
--     If < 180, this gives degrees latitude East
DELIMITER $$
CREATE FUNCTION RA2Long(`RA` DECIMAL(7,5))
RETURNS DECIMAL(8,5)
DETERMINISTIC
	BEGIN
		DECLARE longitude DECIMAL(8,5);
		IF (`RA`*15 >= 180) THEN
			SET longitude = CAST(`RA`*15 - 360 AS DECIMAL(8,5));
		ELSE
			SET longitude = CAST(`RA`*15 AS DECIMAL(8,5));
		END IF;
	RETURN (longitude);
END$$
DELIMITER ;

-- Convert Dec to Latitude
--     If > 0, this gives the latitude N
--     If < 0, multiply by -1.  This gives latitude S
DELIMITER $$
CREATE FUNCTION Dec2Lat(`Dec` DECIMAL(7,5))
RETURNS DECIMAL(7,5)
DETERMINISTIC
	BEGIN
		DECLARE latitude DECIMAL(7,5);
		IF (`Dec` < 0) THEN
			SET latitude = CAST(`Dec` AS DECIMAL(7, 5));
		ELSE
			SET latitude = CAST(`Dec` AS DECIMAL(7, 5));
		END IF;
	RETURN (latitude);
END$$
DELIMITER ;


-- Populate data into the Resides table.
INSERT INTO Resides 
SELECT
	Star.HipparcosID,
    Star.ConstellationID
FROM
	Star,
    Constellation
WHERE
	Star.ConstellationID = Constellation.ConstellationID;