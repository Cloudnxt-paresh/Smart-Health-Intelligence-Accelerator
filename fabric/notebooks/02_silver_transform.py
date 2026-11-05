# Fabric notebook source: Silver transformations
from pyspark.sql import functions as F
from pyspark.sql import types as T

silver_patients = (
    spark.table("bronze_patients")
    .select(
        F.trim("PatientID").alias("PatientID"),
        F.trim("PatientName").alias("PatientName"),
        F.to_date("DateOfBirth").alias("DateOfBirth"),
        F.trim("Sex").alias("Sex"),
        F.trim("City").alias("City"),
        F.trim("DataLabel").alias("DataLabel"),
    )
    .dropDuplicates(["PatientID"])
)
silver_patients.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_patients")

silver_screenings = (
    spark.table("bronze_screenings")
    .select(
        F.trim("ScreeningID").alias("ScreeningID"),
        F.trim("PatientID").alias("PatientID"),
        F.to_date("ScreeningDate").alias("ScreeningDate"),
        F.trim("ScreeningType").alias("ScreeningType"),
        F.trim("Facility").alias("Facility"),
        F.trim("DataLabel").alias("DataLabel"),
    )
    .dropDuplicates(["ScreeningID"])
)
silver_screenings.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_screenings")

silver_parameters = (
    spark.table("bronze_parameters")
    .select(
        F.trim("ParameterCode").alias("ParameterCode"),
        F.trim("ParameterName").alias("ParameterName"),
        F.trim("TestCategory").alias("TestCategory"),
        F.trim("Unit").alias("Unit"),
        F.col("ReferenceLow").cast(T.DoubleType()).alias("ReferenceLow"),
        F.col("ReferenceHigh").cast(T.DoubleType()).alias("ReferenceHigh"),
        F.trim("PlainLanguageMeaning").alias("PlainLanguageMeaning"),
        F.trim("RangeNote").alias("RangeNote"),
    )
    .dropDuplicates(["ParameterCode"])
)
silver_parameters.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_parameters")

lab = (
    spark.table("bronze_lab_results")
    .withColumn("MeasuredValue", F.col("MeasuredValue").cast(T.DoubleType()))
    .withColumn("ReferenceLow", F.col("ReferenceLow").cast(T.DoubleType()))
    .withColumn("ReferenceHigh", F.col("ReferenceHigh").cast(T.DoubleType()))
    .withColumn("TestDate", F.to_date("TestDate"))
    .withColumn(
        "CalculatedStatus",
        F.when(F.col("MeasuredValue").isNull(), "MISSING")
        .when(F.col("ReferenceLow").isNull() | F.col("ReferenceHigh").isNull(), "NO REFERENCE RANGE")
        .when(F.col("MeasuredValue") < F.col("ReferenceLow"), "LOW")
        .when(F.col("MeasuredValue") > F.col("ReferenceHigh"), "HIGH")
        .otherwise("WITHIN RANGE"),
    )
    .withColumn("IsOutsideRange", F.when(F.col("CalculatedStatus").isin("HIGH", "LOW"), 1).otherwise(0))
    .withColumn(
        "StatusValidation",
        F.when(F.upper(F.trim(F.col("ResultStatus"))) == F.col("CalculatedStatus"), "MATCH").otherwise("CHECK"),
    )
    .dropDuplicates(["ResultID"])
)
lab.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_lab_results")

observations = spark.table("bronze_clinical_observations").dropDuplicates(["ObservationID"])
observations.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("silver_clinical_observations")

print("Silver transformation completed")
