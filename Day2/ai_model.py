import numpy as np

def predict_risk(s1, s2, s3):
    avg = (s1 + s2 + s3) / 3

    if avg < 40:
        return "HIGH RISK ⚠️"
    elif avg < 60:
        return "MEDIUM RISK ⚡"
    else:
        return "SAFE ✅"