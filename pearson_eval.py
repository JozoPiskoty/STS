import json
from scipy.stats import pearsonr

with open("experiment_scores1.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

human_scores = data["human"]
results = data["results"]
configs = data["configs"]

scores = []

for i in range(len(configs)):
    model_scores = results[str(i)]
    r = pearsonr(human_scores, model_scores)[0]
    scores.append((i, r, configs[i]))

scores.sort(key=lambda x: x[1], reverse=True)

for i, r, config in scores:
    print(f"{r:.4f} -> {config}")
