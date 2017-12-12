import sqlite3


objects_script = """
CREATE TABLE IF NOT EXISTS Settings (
Name TEXT,
DateOfBirth DATE,
VDOT REAL,
MaxHR INT);

CREATE TABLE IF NOT EXISTS SchedulePlan (
SchedulePlanID INTEGER PRIMARY KEY,
ScheduleName TEXT UNIQUE NOT NULL);

CREATE TABLE IF NOT EXISTS Workout (
WorkoutID INTEGER PRIMARY KEY,
Name TEXT UNIQUE NOT NULL,
WorkoutJSON TEXT NOT NULL,
FileName TEXT NULL,
SerialNumber TEXT NULL
IsCustom INT NOT NULL,
CHECK (IsCustom IN (0,1));

CREATE TABLE IF NOT EXISTS ScheduleWorkout (
ScheduleWorkoutID INTEGER PRIMARY KEY,
SchedulePlanID INT NOT NULL,
WorkoutID INT NOT NULL,
DaysFromEnd INT NOT NULL,
FOREIGN KEY(WorkoutID) REFERENCES Workout(WorkoutID),
FOREIGN KEY(SchedulePlanID) REFERENCES SchedulePlan(SchedulePlanID));

CREATE TABLE IF NOT EXISTS Shoe (
ShoeID INTEGER PRIMARY KEY,
ShoeName TEXT UNIQUE NOT NULL,
StartDate DATE DEFAULT (datetime('now','localtime')),
DateRetired DATE,
PreviousMiles REAL
PreviousKM REAL,
IsDefault INT NOT NULL,
CHECK (IsDefault IN (0,1))

CREATE TABLE IF EXISTS RunType (
RunTypeID INTEGER PRIMARY KEY,
RunTypeName TEXT UNIQUE)

CREATE TABLE IF EXISTS Race (
RaceID INTEGER PRIMARY KEY,
RaceName TEXT UNIQUE,
RaceDistanceID INT,
FOREIGN KEY(RaceDistanceID) REFERENCES RaceDistance(RaceDistanceID))

CREATE TABLE IF EXISTS RaceDetail (
RaceDetailID INTEGER PRIMARY KEY,
RaceID INT,
RaceDate DATE,
GoalTime DATE,
ActualTime DATE,
FOREIGN KEY(RaceID) REFERENCES Race(RaceID))

CREATE TABLE IF NOT EXISTS Diary (
DiaryID INTEGER PRIMARY KEY,
DiaryDate DATE NOT NULL,
DiaryTime DATE NOT NULL,
RunTypeID INT,
DistanceMiles REAL,
DistanceKM REAL,
SpeedMPH REAL,
SpeedKPH REAL,
PaceMiles DATE,
PaceKM REAL,
AverageHR INT,
ShoeID INT,
ScheduleWorkoutID INT,
Effort INT,
RunRating INT,
RaceDetailID INT,
IsDeleted INT,
CHECK (IsDeleted IN (0,1),
CHECK (Effort BETWEEN 1 AND 10),
CHECK (RunRating BETWEEN 1 AND 10),
CHECK (AverageHR BETWEEN 1 AND 250),
FOREIGN KEY(RunTypeID) REFERENCES RunType(RunTypeID),
FOREIGN KEY(ScheduleWorkoutID) REFERENCES ScheduleWorkout(ScheduleWorkoutID),
FOREIGN KEY(ShoeID) REFERENCES Shoe(ShoeID),
FOREIGN KEY(RaceDetailID) REFERENCES RaceDetail(RaceDetailID)
)
"""


def create_db(path):
    """Creates the database in the given path."""
    try:
        return sqlite3.connect(path)
    except Exception as e:
        print('Unable to create database: ', e)


def deploy_database(path):
    """Creates database and deploys objects."""
    try:
        db = create_db(path)
        db.executescript(objects_script)
    except Exception as e:
        print('Unable to create database: ', e)

