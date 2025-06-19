import requests
import random
import os

STATS_API_URL = os.getenv("STATS_API_URL", "http://127.0.0.1:8000")

random.seed()
for model in ["GPT", "Llama", "Mistral"]:
  for stats in range(1, random.randint(20, 100)):
    requests.post(f"{STATS_API_URL}/stats", json = {
      "name": model,
      "version": "v1",
      "prediction_accuracy": random.random(),
      "drift": random.random(),
      "inference_time": random.random() * 100,
    })
