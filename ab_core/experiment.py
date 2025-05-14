# ab_core/experiment.py

import uuid
from datetime import datetime

class Experiment:
    def __init__(self, name, variants):
        self.id = str(uuid.uuid4())
        self.name = name
        self.variants = variants
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "variants": self.variants,
            "created_at": self.created_at.isoformat()
        }

# Optionally: manage a registry of experiments
EXPERIMENTS = {}

def create_experiment(name, variants):
    experiment = Experiment(name, variants)
    EXPERIMENTS[experiment.id] = experiment
    return experiment

def list_experiments():
    return [exp.to_dict() for exp in EXPERIMENTS.values()]
