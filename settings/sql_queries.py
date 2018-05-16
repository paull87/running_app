
vdot_racetimes = """
SELECT
    VDOT,
    [1500],
    Mile,
    [2Mile],
    [3000],
    [5000],
    [10K],
    [15K],
    [10Mile],
    HalfMarathon,
    Marathon
FROM VDOTRaceTimes;"""

vdot_paces = """
SELECT
    VDOT,
    Unit,
    Recovery,
    Easy,
    Long,
    Threshold,
    Interval,
    Repetition,
    [1500],
    Mile,
    [2Mile],
    [3000],
    [5000],
    [10K],
    [15K],
    [10Mile],
    HalfMarathon,
    Marathon
FROM VDOTPaces;"""

vdot_range_population = """
CREATE TEMP TABLE _VDOTRange(VDOT INT, Times INT);

INSERT INTO _VDOTRange(VDOT, Times)
SELECT VDOT, [{0}] FROM VDOTRaceTimes
WHERE [{0}] <= {1} ORDER BY VDOT ASC LIMIT 1;

INSERT INTO _VDOTRange(VDOT, Times)
SELECT VDOT, [{0}] FROM VDOTRaceTimes
WHERE [{0}] >= {1} ORDER BY VDOT DESC LIMIT 1;
"""

vdot_range = """
SELECT MAX(VDOT), MAX(Times), MIN(Times)
FROM _VDOTRange;
"""

clear_table = "DROP TABLE _VDOTRange;"


insert_vdot = """
INSERT INTO VDOTHistory (VDOT)
VALUES(?);"""

update_settings = """
UPDATE Settings
SET {} = ?;
"""

update_race_times = """
UPDATE VDOTRacePace
SET
    Time = ?,
    MilePace = ?,
    KMPace = ?
WHERE DistanceID IN
    (SELECT DistanceID
    FROM Distance
    WHERE Name = ?);
"""

update_training_paces = """
UPDATE TrainingInterval
SET
    MilePace = ?,
    KMPace = ?
WHERE
    Name = ?;
"""

get_current_settings = """
SELECT
COALESCE(VDOTHistory.VDOT, 0) AS VDOT,
MaxHR,
Units
FROM Settings
LEFT JOIN VDOTHistory
    ON Settings.VDOTHistoryID = VDOTHistory.VDOTHistoryID;
"""

get_hr_zones = """
SELECT
LOWER(Name) as name,
HRZoneLow as low,
HRZoneHigh as high
FROM TrainingInterval;
"""

get_distances = """
SELECT
    Name,
    KM,
    Miles
FROM Distance;"""

get_race_paces = """
SELECT
    Distance.Name AS Distance,
    VDOTRacePace.Time,
    VDOTRacePace.MilePace AS Mile,
    VDOTRacePace.KMPace AS KM
FROM VDOTRacePace
INNER JOIN Distance
    ON VDOTRacePace.DistanceID = Distance.DistanceID;"""

get_training_paces = """
SELECT
    Name AS Distance,
    MilePace AS Mile,
    KMPace AS KM
FROM TrainingInterval;"""

get_targets = """
SELECT
    LOWER(Name) AS Name,
    DefaultTarget,
    HRZoneLow,
    HRZoneHigh,
    [{0}Pace] AS Pace
FROM
    TrainingInterval
UNION ALL
SELECT
    LOWER(Distance.Name) AS Distance,
    'pace' as DefaultTarget,
    NULL AS HRZoneLow,
    NULL AS HRZoneHigh,
    VDOTRacePace.[{0}Pace] AS Pace
FROM VDOTRacePace
INNER JOIN Distance
    ON VDOTRacePace.DistanceID = Distance.DistanceID;"""

get_workout_templates = """
SELECT
    Name,
    WorkoutJSON,
    FileName,
    SerialNumber,
    IsCustom
FROM
    Workout;"""

update_workout = """
UPDATE Workout
SET
    FileName = ?,
    SerialNumber = ?
WHERE
    Name = ?
"""

get_schedule_workouts = """
SELECT
    ScheduleName,
    Schedule.ScheduleID,
    ScheduleWorkout.ScheduleWorkoutID,
    Workout.Name AS WorkoutName,
    Workout.WorkoutID,
    DaysFromEnd,
    WorkoutWeek,
    WorkoutWeekDay,
    Distance.DistanceID,
    Distance.Name AS RaceDistance
FROM ScheduleWorkout
INNER JOIN Schedule
    ON ScheduleWorkout.ScheduleID = Schedule.ScheduleID
LEFT JOIN Workout
    ON ScheduleWorkout.WorkoutID = Workout.WorkoutID
LEFT JOIN Distance
    ON ScheduleWorkout.RaceDistanceID = Distance.DistanceID
WHERE ScheduleName = ?;"""

add_planned_schedule = """
INSERT INTO PlannedSchedule(ScheduleID, StartDate, EndDate)
VALUES (
    ?,
    ?,
    ?);
"""

add_schedule_plan = """
INSERT INTO SchedulePlan(ScheduleWorkoutID, ScheduleDate, RaceDetailID, PlannedScheduleID, Completed)
VALUES(
    ?,
    ?,
    ?,
    ?,
    0);"""

add_default_schedule_race = """
INSERT INTO RaceDetail(RaceID, RaceDate)
SELECT RaceID, ?
FROM Race
WHERE
    DistanceID = ?
    AND RaceName LIKE 'Unknown%'
    AND NOT EXISTS (
        SELECT 1 FROM RaceDetail WHERE RaceDate = ?);
"""


add_schedule_race = """
INSERT INTO RaceDetail(RaceID, RaceDate)
SELECT RaceID, ?
FROM Race
WHERE
    DistanceID = ?
    AND RaceName = ?;
"""

get_calendar_range = """
SELECT
    ItemType,
    ItemID,
    ItemDate AS "ItemDate [timestamp]",
    ItemName,
    RaceGoal,
    FinishTime
FROM Calendar
WHERE
    ItemDate >= ?
    AND ItemDate < ?
ORDER BY
    ItemDate,
    ItemPriority;
"""

get_shoe_list = """
SELECT
    ShoeID,
    ShoeName,
    IsDefault
FROM Shoe
WHERE
    DateRetired IS NULL;
"""

"""
CREATE TABLE IF NOT EXISTS ScheduleWorkout (
ScheduleWorkoutID INTEGER PRIMARY KEY,
ScheduleID INT NOT NULL,
WorkoutID INT NULL,
DaysFromEnd INT NOT NULL,
WorkoutWeek INT NOT NULL,
WorkoutWeekDay INT NOT NULL,
Race TEXT,
FOREIGN KEY(WorkoutID) REFERENCES Workout(WorkoutID),
FOREIGN KEY(ScheduleID) REFERENCES Schedule(ScheduleID));

CREATE TABLE IF NOT EXISTS SchedulePlan (
SchedulePlanID INTEGER PRIMARY KEY,
PlannedScheduleID INT NOT NULL,
ScheduleWorkoutID INT NOT NULL,
ScheduleDate DATE NOT NULL,
RaceDetailID INT NULL,
Completed INT NOT NULL,
FOREIGN KEY(PlannedScheduleID) REFERENCES PlannedSchedule(PlannedScheduleID),
FOREIGN KEY(ScheduleWorkoutID) REFERENCES ScheduleWorkout(ScheduleWorkoutID),
FOREIGN KEY(RaceDetailID) REFERENCES RaceDetail(RaceDetailID));"""