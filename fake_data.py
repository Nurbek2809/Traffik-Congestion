import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os
import random

fake = Faker()
np.random.seed(42)
random.seed(42)

# =========================
# SOZLAMALAR
# =========================
OUTPUT_DIR = "traffic_mock_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_REGIONS = 80
NUM_ACCIDENTS = 1500
NUM_CONGESTION = 3000
NUM_WEATHER = 2000

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

# =========================
# YORDAMCHI FUNKSIYALAR
# =========================

def random_datetime(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def get_time_period(dt):
    hour = dt.hour
    if 7 <= hour <= 9:
        return "Morning Peak"
    elif 17 <= hour <= 20:
        return "Evening Peak"
    elif 22 <= hour or hour <= 5:
        return "Night"
    else:
        return "Normal"


def weighted_choice(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]


# =========================
# 1. REGIONS TABLE
# =========================

cities = ["Toshkent", "Samarqand", "Buxoro", "Andijon", "Namangan", "Farg'ona"]
districts = [
    "Yunusobod", "Chilonzor", "Mirzo Ulug'bek", "Yakkasaroy", "Shayxontohur",
    "Olmazor", "Sergeli", "Bektemir", "Mirobod", "Uchtepa"
]

streets = [
    "Amir Temur ko'chasi", "Navoiy ko'chasi", "Mustaqillik shoh ko'chasi",
    "Buyuk Ipak Yo'li", "Bunyodkor shoh ko'chasi", "Beruniy ko'chasi",
    "Shota Rustaveli ko'chasi", "Farg'ona yo'li", "Bobur ko'chasi",
    "Qatortol ko'chasi", "Kichik halqa yo'li", "Toshkent halqa yo'li"
]

regions = []

for i in range(1, NUM_REGIONS + 1):
    city = random.choice(cities)
    district = random.choice(districts)
    street = random.choice(streets)

    latitude = round(np.random.uniform(40.95, 41.45), 6)
    longitude = round(np.random.uniform(69.05, 69.55), 6)

    location = f"{city}, {district}, {street}"

    regions.append({
        "RegionID": i,
        "City": city,
        "District": district,
        "StreetName": street,
        "Location": location,
        "Latitude": latitude,
        "Longitude": longitude
    })

regions_df = pd.DataFrame(regions)

# =========================
# 2. WEATHER CONDITIONS TABLE
# =========================

weather_types = [
    ("Clear", 45),
    ("Cloudy", 20),
    ("Rain", 18),
    ("Snow", 7),
    ("Fog", 6),
    ("Storm", 4)
]

weather_data = []

for i in range(1, NUM_WEATHER + 1):
    dt = random_datetime(START_DATE, END_DATE)
    region = regions_df.sample(1).iloc[0]
    weather = weighted_choice(weather_types)

    if weather == "Clear":
        visibility = round(np.random.uniform(8, 15), 1)
        temperature = round(np.random.uniform(15, 38), 1)
    elif weather == "Rain":
        visibility = round(np.random.uniform(3, 9), 1)
        temperature = round(np.random.uniform(5, 25), 1)
    elif weather == "Snow":
        visibility = round(np.random.uniform(2, 7), 1)
        temperature = round(np.random.uniform(-10, 5), 1)
    elif weather == "Fog":
        visibility = round(np.random.uniform(0.5, 4), 1)
        temperature = round(np.random.uniform(-2, 12), 1)
    elif weather == "Storm":
        visibility = round(np.random.uniform(1, 5), 1)
        temperature = round(np.random.uniform(5, 28), 1)
    else:
        visibility = round(np.random.uniform(5, 12), 1)
        temperature = round(np.random.uniform(5, 30), 1)

    weather_data.append({
        "WeatherID": i,
        "DateTime": dt,
        "RegionID": region["RegionID"],
        "Location": region["Location"],
        "WeatherType": weather,
        "Visibility": visibility,
        "Temperature": temperature
    })

weather_df = pd.DataFrame(weather_data)

# =========================
# 3. ACCIDENTS TABLE
# =========================

accident_causes = [
    ("Speeding", 28),
    ("Red Light Violation", 18),
    ("DUI", 8),
    ("Distracted Driving", 15),
    ("Bad Road Condition", 10),
    ("Poor Visibility", 8),
    ("Weather Condition", 7),
    ("Pedestrian Error", 6)
]

severity_levels = [
    ("Minor", 60),
    ("Major", 30),
    ("Fatal", 10)
]

accidents = []

for i in range(1, NUM_ACCIDENTS + 1):
    dt = random_datetime(START_DATE, END_DATE)
    region = regions_df.sample(1).iloc[0]
    cause = weighted_choice(accident_causes)

    # Noqulay ob-havo bo'lsa og'irlik oshishi mumkin
    weather = weighted_choice(weather_types)

    if weather in ["Fog", "Snow", "Storm"]:
        severity = weighted_choice([
            ("Minor", 45),
            ("Major", 38),
            ("Fatal", 17)
        ])
    else:
        severity = weighted_choice(severity_levels)

    if severity == "Minor":
        injuries = np.random.randint(0, 3)
        fatalities = 0
        severity_score = 1
    elif severity == "Major":
        injuries = np.random.randint(1, 8)
        fatalities = np.random.choice([0, 1], p=[0.85, 0.15])
        severity_score = 2
    else:
        injuries = np.random.randint(1, 10)
        fatalities = np.random.randint(1, 4)
        severity_score = 3

    accidents.append({
        "AccidentID": i,
        "DateTime": dt,
        "RegionID": region["RegionID"],
        "Location": region["Location"],
        "Cause": cause,
        "Severity": severity,
        "SeverityScore": severity_score,
        "Weather": weather,
        "Injuries": injuries,
        "Fatalities": fatalities
    })

accidents_df = pd.DataFrame(accidents)

# =========================
# 4. CONGESTION TABLE
# =========================

congestion_causes = [
    ("Peak Hours", 35),
    ("Signal Timing", 18),
    ("Construction", 14),
    ("Road Blockage", 10),
    ("Accident", 12),
    ("High Vehicle Density", 11)
]

congestion_data = []

for i in range(1, NUM_CONGESTION + 1):
    dt = random_datetime(START_DATE, END_DATE)
    region = regions_df.sample(1).iloc[0]
    time_period = get_time_period(dt)
    cause = weighted_choice(congestion_causes)

    if time_period in ["Morning Peak", "Evening Peak"]:
        speed = round(np.random.uniform(5, 35), 1)
        duration = round(np.random.uniform(20, 120), 1)
        vehicle_count = np.random.randint(700, 2500)
        density = round(np.random.uniform(80, 220), 1)
        capacity_utilization = round(np.random.uniform(70, 115), 1)
    elif time_period == "Night":
        speed = round(np.random.uniform(35, 80), 1)
        duration = round(np.random.uniform(5, 35), 1)
        vehicle_count = np.random.randint(100, 700)
        density = round(np.random.uniform(10, 80), 1)
        capacity_utilization = round(np.random.uniform(15, 60), 1)
    else:
        speed = round(np.random.uniform(20, 60), 1)
        duration = round(np.random.uniform(10, 75), 1)
        vehicle_count = np.random.randint(300, 1500)
        density = round(np.random.uniform(40, 150), 1)
        capacity_utilization = round(np.random.uniform(40, 95), 1)

    congestion_data.append({
        "CongestionID": i,
        "DateTime": dt,
        "RegionID": region["RegionID"],
        "Location": region["Location"],
        "Speed": speed,
        "Duration": duration,
        "VehicleCount": vehicle_count,
        "VehicleDensityPerKm": density,
        "RoadCapacityUtilization": capacity_utilization,
        "PeakPeriod": time_period,
        "Cause": cause
    })

congestion_df = pd.DataFrame(congestion_data)

# =========================
# 5. TRAFFIC VIOLATIONS TABLE
# =========================

violation_types = [
    ("Speeding", 32),
    ("Red Light", 22),
    ("DUI", 8),
    ("Illegal Parking", 12),
    ("Wrong Lane", 10),
    ("No Seat Belt", 9),
    ("Phone Usage", 7)
]

vehicle_types = [
    ("Car", 55),
    ("Truck", 12),
    ("Bus", 10),
    ("Motorcycle", 15),
    ("Taxi", 8)
]

violations = []

violation_id = 1

for _, accident in accidents_df.iterrows():
    # Har bir avariya uchun 0 dan 3 gacha qoida buzilishi
    num_violations = np.random.choice([0, 1, 2, 3], p=[0.25, 0.45, 0.22, 0.08])

    for _ in range(num_violations):
        violation_type = weighted_choice(violation_types)
        vehicle_type = weighted_choice(vehicle_types)

        if violation_type == "DUI":
            penalty = np.random.randint(1500000, 5000000)
        elif violation_type == "Red Light":
            penalty = np.random.randint(500000, 2000000)
        elif violation_type == "Speeding":
            penalty = np.random.randint(300000, 1500000)
        else:
            penalty = np.random.randint(150000, 900000)

        violations.append({
            "ViolationID": violation_id,
            "AccidentID": accident["AccidentID"],
            "Type": violation_type,
            "PenaltyAmount": penalty,
            "VehicleType": vehicle_type
        })

        violation_id += 1

violations_df = pd.DataFrame(violations)

# =========================
# 6. INFRASTRUCTURE TABLE
# =========================

road_conditions = [
    ("Excellent", 18),
    ("Good", 35),
    ("Average", 25),
    ("Poor", 15),
    ("Critical", 7)
]

improvement_options = {
    "Excellent": "No major improvement needed",
    "Good": "Regular monitoring",
    "Average": "Road marking and signal optimization",
    "Poor": "Road repair and traffic sign installation",
    "Critical": "Urgent reconstruction and traffic control"
}

infrastructure = []

for i, region in regions_df.iterrows():
    condition = weighted_choice(road_conditions)

    infrastructure.append({
        "InfrastructureID": i + 1,
        "RegionID": region["RegionID"],
        "Location": region["Location"],
        "Condition": condition,
        "ImprovementNeeded": improvement_options[condition]
    })

infrastructure_df = pd.DataFrame(infrastructure)

# =========================
# 7. RISK SCORE TABLE
# Qo'shimcha jadval: Power BI uchun juda foydali
# =========================

accident_summary = accidents_df.groupby("RegionID").agg(
    AccidentCount=("AccidentID", "count"),
    TotalInjuries=("Injuries", "sum"),
    TotalFatalities=("Fatalities", "sum"),
    AvgSeverityScore=("SeverityScore", "mean")
).reset_index()

congestion_summary = congestion_df.groupby("RegionID").agg(
    AvgSpeed=("Speed", "mean"),
    AvgCongestionDuration=("Duration", "mean"),
    AvgVehicleDensity=("VehicleDensityPerKm", "mean")
).reset_index()

risk_df = regions_df.merge(accident_summary, on="RegionID", how="left")
risk_df = risk_df.merge(congestion_summary, on="RegionID", how="left")

risk_df = risk_df.fillna(0)

risk_df["CombinedRiskScore"] = (
    risk_df["AccidentCount"] * risk_df["AvgSeverityScore"] +
    risk_df["AvgCongestionDuration"] +
    risk_df["TotalFatalities"] * 10
).round(2)

risk_df["RiskLevel"] = pd.cut(
    risk_df["CombinedRiskScore"],
    bins=[-1, 30, 60, 100, 100000],
    labels=["Low", "Medium", "High", "Critical"]
)

# =========================
# 8. CSV FAYLLARNI SAQLASH
# =========================

regions_df.to_csv(f"{OUTPUT_DIR}/Regions.csv", index=False, encoding="utf-8-sig")
weather_df.to_csv(f"{OUTPUT_DIR}/WeatherConditions.csv", index=False, encoding="utf-8-sig")
accidents_df.to_csv(f"{OUTPUT_DIR}/Accidents.csv", index=False, encoding="utf-8-sig")
congestion_df.to_csv(f"{OUTPUT_DIR}/Congestion.csv", index=False, encoding="utf-8-sig")
violations_df.to_csv(f"{OUTPUT_DIR}/TrafficViolations.csv", index=False, encoding="utf-8-sig")
infrastructure_df.to_csv(f"{OUTPUT_DIR}/Infrastructure.csv", index=False, encoding="utf-8-sig")
risk_df.to_csv(f"{OUTPUT_DIR}/RiskAnalysis.csv", index=False, encoding="utf-8-sig")

print("Data muvaffaqiyatli yaratildi!")
print(f"Fayllar joylashuvi: {OUTPUT_DIR}")

print("\nYaratilgan fayllar:")
print("1. Regions.csv")
print("2. Accidents.csv")
print("3. Congestion.csv")
print("4. TrafficViolations.csv")
print("5. Infrastructure.csv")
print("6. WeatherConditions.csv")
print("7. RiskAnalysis.csv")