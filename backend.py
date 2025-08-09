from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

class Prop(BaseModel):
    player_name: str
    kill_line: float
    hs_line: float
    salary: float
    map_count: int

@app.get("/")
def home():
    return {"status": "Bolt backend live"}

@app.get("/board")
def get_board():
    # Simulated fetch (replace with your real scraping or data source)
    sample_data = [
        {"player": "device", "kill_line": 32.5, "hs_line": 11, "salary": 14, "map_count": 2, "kpr": 0.82, "hs_percent": 0.34},
        {"player": "jabbi", "kill_line": 31.5, "hs_line": 18.5, "salary": 15, "map_count": 2, "kpr": 0.78, "hs_percent": 0.40},
        {"player": "stavn", "kill_line": 30.5, "hs_line": 14.5, "salary": 13, "map_count": 2, "kpr": 0.80, "hs_percent": 0.38},
    ]

    props_with_value = []
    for prop in sample_data:
        expected_kills = prop["kpr"] * (prop["map_count"] * 24)  # assume ~24 rounds per map
        value_score = round((prop["hs_line"] * 0.65 + (expected_kills) * 0.35) - prop["salary"], 2)
        props_with_value.append({
            **prop,
            "expected_kills": round(expected_kills, 2),
            "value_score": value_score,
            "good": value_score >= 12.5  # flag for good props
        })

    # Sort by value_score (best to worst)
    sorted_props = sorted(props_with_value, key=lambda x: x["value_score"], reverse=True)

    return {
        "status": "success",
        "props": sorted_props
    }

@app.post("/evaluate")
def evaluate_prop(prop: Prop):
    expected_kills = prop.kill_line / prop.map_count  # placeholder
    value_score = round((prop.hs_line * 0.65 + (expected_kills) * 0.35) - prop.salary, 2)

    return {
        "verdict": "Good value" if value_score >= 8 else "Low value",  # lowered threshold
        "value_score": value_score,
        "expected_kills": expected_kills,
        "used_kpr": None,  # Replace when you pull actual stats
        "used_hs": None,
        "notes": "Evaluation complete"
    }
