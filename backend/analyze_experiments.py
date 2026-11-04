import json
import numpy as np

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\experiment_results.json', 'r') as f:
    data = json.load(f)

pA = np.array(data['pA']) # Py Bicubic
pC = np.array(data['pC']) # Py Nearest
pD = np.array(data['pD']) # JS Bilinear
pE = np.array(data['pE']) # JS Nearest

with open(r'C:\Projects\GroWise_Fullstack\GroWise\backend\models\class_indices.json', 'r') as f:
    class_indices = json.load(f)
    classes = {int(v): k for k, v in class_indices.items()}

def report(name, probs):
    idx = np.argmax(probs)
    conf = np.max(probs)
    top5_idx = np.argsort(probs)[-5:][::-1]
    top5 = [(int(i), classes[i], float(probs[i])) for i in top5_idx]
    
    print(f"\n{name}")
    print(f"Predicted Class: {classes[idx]}")
    print(f"Predicted Index: {idx}")
    print(f"Confidence: {conf:.6f}")
    print(f"Top 5:")
    for i, n, c in top5:
        print(f"  {i:2d} ({n}): {c:.6f}")
    print(f"Raw Vector:\n[{', '.join(f'{x:.4f}' for x in probs)}]")

report("Experiment A (Python Bicubic)", pA)
report("Experiment C (Python Nearest)", pC)
report("Experiment D (JS Bilinear)", pD)
report("Experiment E (JS Nearest)", pE)

def compare(p1, p2, name):
    diff = np.abs(p1 - p2)
    print(f"\n{name}")
    print(f"Max Absolute Diff:  {np.max(diff):.6f}")
    print(f"Mean Absolute Diff: {np.mean(diff):.6f}")
    print(f"RMSE:               {np.sqrt(np.mean(diff**2)):.6f}")

compare(pA, pD, "Python (Bicubic) vs JS (Bilinear) [CURRENT PRODUCTION MISMATCH]")
compare(pC, pE, "Python (Nearest) vs JS (Nearest) [CONTROLLED MATCH]")
