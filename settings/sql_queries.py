
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
Name,
DateOfBirth,
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
INSERT INTO PlannedSchedule(ScheduleID, StartDate, EndDate, ScheduleName, PlanVDOT)
VALUES (
    ?,
    ?,
    ?,
    ?,
    ?);
"""

get_schedules = """
SELECT ScheduleName FROM Schedule;"""

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
    Shoe.ShoeID,
    ShoeName,
    IsDefault
FROM Shoe
WHERE DateRetired IS NULL;
"""

get_shoe_list_complete = """
SELECT
    Shoe.ShoeID,
    ShoeName,
    Brand,
    StartDate,
    DateRetired,
    COALESCE(SUM(DistanceMiles), 0.0) AS MilesRun,
    COALESCE(SUM(DistanceKM), 0.0) AS KMRun,
    COALESCE(SUM(RunTime), 0.0) AS TimeRunning,
    COALESCE(MAX(DistanceMiles), 0.0) AS LongestRunMile,
    COALESCE(MAX(DistanceKM), 0.0) AS LongestRunKM,
    IsDefault
FROM Shoe
LEFT JOIN Diary
    ON Diary.ShoeID = Shoe.ShoeID
WHERE Shoe.ShoeID > 0;
"""

delete_schedule_plan_workouts = """
UPDATE SchedulePlan
SET IsDeleted = 1
WHERE PlannedScheduleID = ?;"""

delete_schedule_plan = """
UPDATE PlannedSchedule
SET IsDeleted = 1
WHERE PlannedScheduleID = ?;"""

add_diary_entry = """
INSERT INTO Diary(DiaryDate,RunTime,RunTypeID,DistanceMiles,DistanceKM,SpeedMPH,SpeedKPH,PaceMiles,PaceKM,AverageHR,
    ShoeID,SchedulePlanID,Effort,RunRating,RaceDetailID,StravaID,IntensityPointsHR,IntensityPointsPace,IsDeleted)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

edit_diary_entry = """
UPDATE Diary
SET 
    DiaryDate = ?,
    RunTime = ?,
    RunTypeID = ?,
    DistanceMiles = ?,
    DistanceKM = ?,
    SpeedMPH = ?,
    SpeedKPH = ?,
    PaceMiles = ?,
    PaceKM = ?,
    AverageHR = ?,
    ShoeID = ?,
    SchedulePlanID = ?,
    Effort = ?,
    RunRating = ?,
    RaceDetailID = ?,
    StravaID = ?,
    IntensityPointsHR = ?,
    IntensityPointsPace = ?,
    IsDeleted = ?
WHERE
    DiaryID = ?;"""

get_run_types = """
SELECT RunTypeID, Name
FROM RunType
ORDER BY Name;"""

get_points = """
SELECT Points
FROM IntensityPoints
WHERE MaxHRPercent >= ?
ORDER BY MaxHRPercent ASC
LIMIT 1;"""

add_shoe = """
INSERT INTO Shoe (ShoeName, Brand, Description, StartDate, DateRetired, PreviousMiles, PreviousKM, IsDefault)
VALUES(?,?,?,?,?,?,?,?);"""

amend_shoe = """
UPDATE Shoe
SET 
    ShoeName = ?, 
    Brand = ?, 
    Description = ?, 
    StartDate = ?, 
    DateRetired = ?, 
    PreviousMiles = ?, 
    PreviousKM = ?, 
    IsDefault = ?
WHERE
    ShoeID = ?;"""

reset_default_shoe = """
UPDATE Shoe
SET IsDefault = 0;"""

get_scheduled_workout_details = """
SELECT  Workout.Name, Workout.WorkoutJSON, Workout.FileName, Workout.SerialNumber, SchedulePlan.ScheduleDate
FROM PlannedSchedule
INNER JOIN SchedulePlan
	ON PlannedSchedule.PlannedScheduleID = SchedulePlan.PlannedScheduleID
INNER JOIN ScheduleWorkout
	on SchedulePlan.ScheduleWorkoutID =  ScheduleWorkout.ScheduleWorkoutID
INNER JOIN Workout
	ON ScheduleWorkout.WorkoutID = Workout.WorkoutID
WHERE
	PlannedSchedule.IsDeleted = 0
	AND SchedulePlan.IsDeleted = 0
	AND SchedulePlan.ScheduleDate >= ?;"""