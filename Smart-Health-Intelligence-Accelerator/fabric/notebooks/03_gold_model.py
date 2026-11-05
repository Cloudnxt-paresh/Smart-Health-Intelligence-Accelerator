# Fabric notebook source: Gold analytical model
from pyspark.sql import functions as F
from pyspark.sql.window import Window

patients = spark.table("silver_patients")
screenings = spark.table("silver_screenings")
parameters = spark.table("silver_parameters")
results = spark.table("silver_lab_results")
observations = spark.table("silver_clinical_observations")

trend_window = Window.partitionBy("PatientID", "ParameterCode").orderBy("TestDate")

gold_patient_results = (
    results
    .join(patients.select("PatientID", "PatientName", "DateOfBirth", "Sex", "City", "DataLabel"), "PatientID", "left")
    .join(screenings.select("ScreeningID", "ScreeningDate", "ScreeningType", "Facility"), "ScreeningID", "left")
    .join(parameters.select("ParameterCode", "PlainLanguageMeaning", "RangeNote"), "ParameterCode", "left")
    .withColumn("PreviousValue", F.lag("MeasuredValue").over(trend_window))
    .withColumn("PreviousTestDate", F.lag("TestDate").over(trend_window))
    .withColumn("ValueChange", F.round(F.col("MeasuredValue") - F.col("PreviousValue"), 2))
    .withColumn(
        "TrendDirection",
        F.when(F.col("PreviousValue").isNull(), "NO PREVIOUS RESULT")
        .when(F.col("MeasuredValue") > F.col("PreviousValue"), "INCREASED")
        .when(F.col("MeasuredValue") < F.col("PreviousValue"), "DECREASED")
        .otherwise("NO CHANGE"),
    )
    .withColumn(
        "StatusDisplay",
        F.when(F.col("CalculatedStatus") == "HIGH", "↑ HIGH")
        .when(F.col("CalculatedStatus") == "LOW", "↓ LOW")
        .when(F.col("CalculatedStatus") == "WITHIN RANGE", "✓ WITHIN RANGE")
        .otherwise(F.col("CalculatedStatus")),
    )
)
gold_patient_results.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_patient_results")

gold_screening_summary = (
    gold_patient_results
    .groupBy("PatientID", "PatientName", "ScreeningID", "ScreeningDate", "ScreeningType", "Facility")
    .agg(
        F.countDistinct("TestCategory").alias("TotalTestCategories"),
        F.count("ResultID").alias("TotalParameters"),
        F.sum(F.when(F.col("CalculatedStatus") == "WITHIN RANGE", 1).otherwise(0)).alias("WithinRangeCount"),
        F.sum(F.when(F.col("CalculatedStatus") == "HIGH", 1).otherwise(0)).alias("HighCount"),
        F.sum(F.when(F.col("CalculatedStatus") == "LOW", 1).otherwise(0)).alias("LowCount"),
        F.sum("IsOutsideRange").alias("OutsideRangeCount"),
    )
    .withColumn("WithinRangePercent", F.round(F.col("WithinRangeCount") / F.col("TotalParameters") * 100, 1))
)
gold_screening_summary.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_screening_summary")

gold_clinical_observations = (
    observations
    .join(patients.select("PatientID", "PatientName"), "PatientID", "left")
    .join(screenings.select("ScreeningID", "ScreeningDate", "Facility"), "ScreeningID", "left")
)
gold_clinical_observations.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_clinical_observations")

print("Gold layer completed")
