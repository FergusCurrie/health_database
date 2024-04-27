# health_database

Code for connecting to MySQL instance to store health records from apple watch, strava

This repo is where data export is converter to clean data and stored to sql. Analysis in seperate repo

| identifier | creationDate | startDate | endDate  | cateogrical_value | numerical_value |
| ---------- | ------------ | --------- | -------- | ----------------- | --------------- |
| VARCHAR    | DATETIME     | DATETIME  | DATETIME | VARCHAR(255)      | FLOAT           |

Apple watch has the following cateogires (numbers give rough indication of frequency from a time period of about 3 months)

- KQuantityTypeIdentifierBasalEnergyBurned 86999
- HKQuantityTypeIdentifierActiveEnergyBurned 86879
- HKQuantityTypeIdentifierHeartRate 64671
- HKQuantityTypeIdentifierDistanceWalkingRunning 57952
- HKQuantityTypeIdentifierStepCount 40429
- HKQuantityTypeIdentifierWalkingSpeed 11937
- HKQuantityTypeIdentifierWalkingStepLength 11934
- HKQuantityTypeIdentifierWalkingDoubleSupportPercentage 11209
- HKQuantityTypeIdentifierFlightsClimbed 10436
- HKQuantityTypeIdentifierAppleExerciseTime 6487
- HKQuantityTypeIdentifierWalkingAsymmetryPercentage 5924
- HKQuantityTypeIdentifierAppleStandTime 5186
- HKQuantityTypeIdentifierRespiratoryRate 5129
- KCategoryTypeIdentifierSleepAnalysis 4041
- HKCategoryTypeIdentifierAppleStandHour 2329
- HKQuantityTypeIdentifierOxygenSaturation 1735
- HKQuantityTypeIdentifierHeartRateVariabilitySDNN 1106
- HKQuantityTypeIdentifierRunningSpeed 930
- HKQuantityTypeIdentifierRunningPower 815
- HKQuantityTypeIdentifierEnvironmentalAudioExposure 728
- HKQuantityTypeIdentifierStairAscentSpeed 545
- HKQuantityTypeIdentifierStairDescentSpeed 516
- HKQuantityTypeIdentifierRunningGroundContactTime 388
- HKQuantityTypeIdentifierRunningVerticalOscillation 388
- HKQuantityTypeIdentifierRunningStrideLength 383
- HKQuantityTypeIdentifierHeadphoneAudioExposure 244
- HKQuantityTypeIdentifierRestingHeartRate 102
- HKQuantityTypeIdentifierAppleSleepingWristTemperature 93
- HKQuantityTypeIdentifierWalkingHeartRateAverage 88
- HKQuantityTypeIdentifierAppleWalkingSteadiness 27
- HKQuantityTypeIdentifierDietaryCaffeine 21
- HKQuantityTypeIdentifierBodyMass 17
- HKQuantityTypeIdentifierVO2Max 15
- HKQuantityTypeIdentifierSixMinuteWalkTestDistance 13
- HKQuantityTypeIdentifierHeartRateRecoveryOneMinute 6
- HKQuantityTypeIdentifierNumberOfAlcoholicBeverages 4
- HKDataTypeSleepDurationGoal 2
- HKCategoryTypeIdentifierSexualActivity 2
- HKQuantityTypeIdentifierHeight 2

The value column in the data is not consistent. Most are numerical, but the following are categorical:

HKCategoryTypeIdentifierAppleStandHour -> HKCategoryValueAppleStandHourIdle or HKCategoryValueAppleStandHourIdle

HKCategoryTypeIdentifierSleepAnalysis -> HKCategoryValueSleepAnalysisAsleepCore, HKCategoryValueSleepAnalysisInBed, HKCategoryValueSleepAnalysisAwake, HKCategoryValueSleepAnalysisAsleepREM, HKCategoryValueSleepAnalysisAsleepDeep

The easiest solution is to have a column to store the category value and a column to store the numerical value, with NULL in the column that is not relevant.

## Setup

MySQL:

```
sudo apt install mysql-server
sudo systemctl status mysql # check if server is up
sudo mysql # connect to MySQL server
create database <name_db=health_records>;
SELECT user, host FROM mysql.user; # check which uses have MySQL access
CREATE user 'fergus'@'localhost'; # create new user
GRANT ALL PRIVILEGES ON *.* TO 'fergus'@'localhost'; # give all privileges
FLUSH PRIVILEGES;
USE health_records;
CREATE TABLE health_records (
    identifier VARCHAR(255),
    creationDate DATETIME,
    startDate DATETIME,
    endDate DATETIME,
    categorical_value VARCHAR(255),
    numerical_value FLOAT
);
```

## Usage

0. (Setup MySQL server)
1. Export data from apple watch to export.zip
2. Copy to root of this dir
3. python3 src/insert_export_into_db.py

python3

```
pip3 install mysql-connector-python
```

## Random notes

- 'export_cda.xml and export.xml'. export_cda.xml: CDA stands for Clinical Document Architecture. Whereas export.xml is all the raw data.

# TODO

- test db + python3 tests
- export.xml wrapped methods e.g. HKQuantityTypeIdentifierHeartRateVariabilitySDNN, HKQuantityTypeIdentifierFlightsClimbed
