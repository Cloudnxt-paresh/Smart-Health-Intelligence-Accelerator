# Fabric notebook source: Bronze load
from pyspark.sql import functions as F

BRONZE_PATH = "Files/bronze"

TABLES = {
    "patients": "patients.csv",
    "screenings": "screenings.csv",
    "parameters": "parameters.csv",
    "lab_results": "lab_results.csv",
    "clinical_observations": "clinical_observations.csv",
}

for table_name, file_name in TABLES.items():
    df = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(f"{BRONZE_PATH}/{file_name}")
    )
    if table_name == "screenings":
        df = df.withColumn("ScreeningDate", F.to_date("ScreeningDate"))
    if table_name in {"lab_results", "clinical_observations"}:
        df = df.withColumn("TestDate", F.to_date("TestDate"))
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(f"bronze_{table_name}")
    )

print("Bronze load completed")
