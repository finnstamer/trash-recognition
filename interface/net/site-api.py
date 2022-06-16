import requests
import json


def addPrediction(classification: str, confidence: float):
    data = {
        "password": "test", "task": "new", "classification": classification, "confidence": confidence,
    } 
    res = requests .post("http://preclassical-princi.000webhostapp.com/api", data=data)
    
    print(res.status_code, res.text)


addPrediction("test", 1)