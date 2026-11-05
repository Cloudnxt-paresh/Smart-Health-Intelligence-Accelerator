TABLES = {
    "bronze_patients": 10,
    "bronze_screenings": 18,
    "bronze_parameters": 32,
    "bronze_lab_results": 576,
    "bronze_clinical_observations": 40,
    "silver_patients": 10,
    "silver_screenings": 18,
    "silver_parameters": 32,
    "silver_lab_results": 576,
    "silver_clinical_observations": 40,
    "gold_patient_results": 576,
    "gold_screening_summary": 18,
    "gold_clinical_observations": 40,
}
for table, expected in TABLES.items():
    actual = spark.table(table).count()
    assert actual == expected, f"{table}: expected {expected}, got {actual}"
    print(f"PASS {table}: {actual}")

validation = spark.table("silver_lab_results").groupBy("StatusValidation").count().collect()
print(validation)
