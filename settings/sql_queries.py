
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
    PrintName,
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
    ON VDOTRacePace.DistanceID = Distance.DistanceID
ORDER BY Distance.Miles;"""

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
WHERE DateRetired IS NULL
ORDER BY 
    IsDefault DESC,
    StartDate DESC;
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
WHERE Shoe.ShoeID > 0
GROUP BY
    Shoe.ShoeID,
    ShoeName,
    Brand,
    StartDate,
    DateRetired,
    IsDefault
ORDER BY
    Shoe.ShoeID,
    ShoeName,
    Brand,
    StartDate,
    DateRetired,
    IsDefault;
"""

get_shoe_detail = """
SELECT
    ShoeID,
    ShoeName,
    Brand,
    Description,
    StartDate,
    DateRetired,
    PreviousMiles,
    PreviousKM,
    isDefault
FROM Shoe
WHERE ShoeID = ?;
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
    ShoeID,SchedulePlanID,Effort,RunRating,RaceDetailID,StravaID,IntensityPointsHR,IntensityPointsPace,Description,IsDeleted)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

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
    Description = ?,
    IsDeleted = ?
WHERE
    DiaryID = ?;"""

get_diary_entry = """
SELECT 
    DiaryID,
    DiaryDate,
    RunTime,
    RunTypeID,
    DistanceMiles,
    DistanceKM,
    SpeedMPH,
    SpeedKPH,
    PaceMiles,
    PaceKM,
    AverageHR,
    ShoeID,
    SchedulePlanID,
    Effort,
    RunRating,
    RaceDetailID,
    StravaID,
    IntensityPointsHR,
    IntensityPointsPace,
    Description,
    IsDeleted
FROM Diary
WHERE
    DiaryID = ?;
"""

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
	AND RaceDetailID IS NULL
	AND SchedulePlan.ScheduleDate >= ?;"""

get_health_stats = """
SELECT Date, WeightKG, WeightLB, RestingHR
FROM HealthStats
WHERE Date = ?;"""

add_health_stats = """
INSERT OR REPLACE INTO HealthStats(Date, WeightKG, WeightLB, RestingHR)
VALUES(?, ?, ?, ?);"""

add_strava_lap = """
INSERT OR REPLACE INTO StravaLap(LapID, StravaID, LapStartDate, LapTime, DistanceMiles, DistanceKM, SpeedMPH, SpeedKPH, PaceMiles, PaceKM, AverageHR, IntensityPointsHR, IntensityPointsPace)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);"""

get_strava_lap = """
SELECT LapID, StravaID, LapStartDate, LapTime, DistanceMiles, DistanceKM, SpeedMPH, SpeedKPH, PaceMiles, PaceKM, AverageHR, IntensityPointsHR, IntensityPointsPace
FROM StravaLap
WHERE StravaID = ?
ORDER BY LapStartDate, LapID;
"""

add_race = """
INSERT INTO Race(RaceName, DistanceID)
SELECT ?, DistanceID
FROM Distance
WHERE Name = ?"""

edit_race = """
UPDATE Race
SET RaceName = ?,
    DistanceID = (SELECT DistanceID FROM Distance WHERE Name = ?)
WHERE RaceID = ?;"""

get_race_list = """
SELECT RaceName, Name
FROM Race
INNER JOIN Distance
    ON Race.DistanceID = Distance.DistanceID
WHERE 
    RaceName NOT LIKE 'Unknown%'
    OR RaceID IN (SELECT RaceID FROM RaceDetail);"""

add_race_detail = """
INSERT INTO RaceDetail(RaceID, RaceDate, GoalTime, ActualTime)
SELECT 
    (SELECT RaceID
    FROM Race
    INNER JOIN Distance
        ON Race.DistanceID = Distance.DistanceID
    WHERE RaceName = ?
    AND Name = ?),
    ?, ?, ?;"""

edit_race_detail = """
UPDATE RaceDetail
SET RaceID = (SELECT RaceID
    FROM Race
    INNER JOIN Distance
        ON Race.DistanceID = Distance.DistanceID
    WHERE RaceName = ?
    AND Name = ?), 
    RaceDate = ?, 
    GoalTime = ?, 
    ActualTime = ?
WHERE RaceDetailID = ?;"""

get_race_detail = """
SELECT RaceDetailID, Race.RaceName, Distance.Name, RaceDate, GoalTime, ActualTime
FROM RaceDetail
INNER JOIN Race
    ON RaceDetail.RaceID = Race.RaceID
INNER JOIN Distance
    ON Race.DistanceID = Distance.DistanceID
WHERE RaceDetailID = ?;"""

get_week_summaries = """
WITH RECURSIVE dates(date) AS (
  VALUES(?)
  UNION ALL
  SELECT date(date, '+1 day')
  FROM dates
  WHERE date < ?
)

SELECT
     AllWeeks.Week, 
     COALESCE(TotalTime, 0) AS TotalTime,
     COALESCE(TotalDistance, 0.0) AS TotalDistance
FROM 
    (SELECT DISTINCT date(date, 'weekday 0', '0 days') AS Week
     FROM dates) AS AllWeeks
LEFT JOIN 
    (SELECT 
         date(DiaryDate, 'weekday 0', '0 days') AS DiaryWeek, 
         SUM(RunTime) AS TotalTime, 
         SUM(DistanceMiles) AS TotalDistance
     FROM Diary
     GROUP BY date(diarydate, 'weekday 0', '0 days')) AS DiaryWeeks
 ON AllWeeks.Week = DiaryWeeks.DiaryWeek
ORDER BY AllWeeks.Week"""

year_stats = """WITH RECURSIVE dates(date) AS (
  VALUES('{current}-01-01')
  UNION ALL
  SELECT date(date, '+1 day')
  FROM dates
  WHERE date(date, '+1 day') < '{next}-01-01'
),
cte_CurrentYear AS (
    SELECT 
        date(DiaryDate) AS DiaryDate, STRFTIME('%m-%d', DiaryDate) AS DiaryDay,
        SUM(distanceMiles) AS TotalDistance,
        SUM(RunTime) AS TotalTime
    FROM Diary
    WHERE DiaryDate >= '{current}-01-01'
    AND DiaryDate < '{next}-01-01'
    GROUP BY date(DiaryDate)
),
cte_PreviousYear AS (
    SELECT date(DiaryDate) AS Diarydate, STRFTIME('%m-%d', DiaryDate) AS DiaryDay,
    SUM(distanceMiles) AS TotalDistance, 
    SUM(RunTime) AS TotalTime
    FROM Diary
    WHERE DiaryDate >= '{previous}-01-01'
    AND DiaryDate < '{current}-01-01'
    GROUP BY date(DiaryDate))

SELECT 
    STRFTIME('%m-%d', dates.date) AS dayOfYear,
    cte_currentYear.TotalDistance AS CurrentDistance,
    (SELECT ROUND(SUM(TotalDistance), 2)
     FROM cte_CurrentYear AS CumCurrent
     WHERE CumCurrent.DiaryDay <= STRFTIME('%m-%d', dates.date)
     AND dates.date <= datetime('now')) AS CumCurrentDistance,
    cte_currentYear.TotalTime AS CurrentTime,
    (SELECT ROUND(SUM(TotalTime), 2)
     FROM cte_CurrentYear AS CumCurrent
     WHERE CumCurrent.DiaryDay <= STRFTIME('%m-%d', dates.date)
     AND dates.date <= datetime('now')) AS CumCurrentTime,
    cte_PreviousYear.TotalDistance AS PreviousDistance,
    (SELECT ROUND(SUM(TotalDistance),2)
     FROM cte_PreviousYear AS CumPrevious
     WHERE CumPrevious.DiaryDay <= STRFTIME('%m-%d', dates.date)) AS CumPreviousDistance,
    cte_PreviousYear.TotalTime AS PreviousTime,
    (SELECT ROUND(SUM(TotalTime),2)
     FROM cte_PreviousYear AS CumPrevious
     WHERE CumPrevious.DiaryDay <= STRFTIME('%m-%d', dates.date)) AS CumPreviousTime
FROM dates
LEFT JOIN cte_CurrentYear
    ON STRFTIME('%m-%d', dates.date) = cte_CurrentYear.DiaryDay
LEFT JOIN cte_PreviousYear
    ON STRFTIME('%m-%d', dates.date) = cte_PreviousYear.DiaryDay
ORDER BY dayOfYear;"""

get_month_summary = """
SELECT 
    COUNT(1) AS TotalRuns,
    COALESCE(SUM(RunTime), 0) AS TotalTime,
    COALESCE(SUM(DistanceMiles),0) AS TotalDistanceMiles,
    COALESCE(SUM(DistanceKM),0) AS TotalDistanceKM,
    COALESCE(AVG(PaceMiles),0) AS AvgPaceMiles,
    COALESCE(AVG(PaceKM),0) AS AvgPaceKM,
    COALESCE(SUM(IntensityPointsHR),0) AS TotalPointsHR,
    COALESCE(AVG(RunRating),0) AS AvgRating
FROM Diary
WHERE diaryDate >= ?
AND diaryDate < ?;
"""

get_year_summaries = """
SELECT
    Stats.Year,
    Stats.TotalRunTime,
    Stats.TotalMiles,
    Stats.TotalKM,
    Stats.AverageHR,
    Stats.AverageIntensityPointsHR,
    HealthStats.AverageKG,
    HealthStats.AverageLB,
    HealthStats.AverageRestingHR
FROM (
    SELECT
        STRFTIME('%Y', DiaryDate) AS Year,
        SUM(RunTime) AS TotalRunTime,
        SUM(DistanceMiles) AS TotalMiles,
        SUM(DistanceKM) AS TotalKM,
        AVG(AverageHR) AS AverageHR,
        AVG(IntensityPointsHR) AS AverageIntensityPointsHR
    FROM Diary
    LEFT JOIN HealthStats
    GROUP BY STRFTIME('%Y', DiaryDate)) AS Stats
LEFT JOIN (
    SELECT
        STRFTIME('%Y', Date) AS Year,
        AVG(WeightKG) AS AverageKG,
        AVG(WeightLB) AS AverageLB,
        AVG(RestingHR) AS AverageRestingHR
    FROM HealthStats
    GROUP BY STRFTIME('%Y', Date)) AS HealthStats
    ON Stats.Year = HealthStats.Year
ORDER BY Stats.Year DESC;"""

update_workout_date = """
UPDATE SchedulePlan
SET ScheduleDate = ?
WHERE SchedulePlanID = ?"""