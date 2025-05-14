# ab_core/tracking.py

import pandas as pd
import random

def simulate_events(num_users, variants, conversion_rates):
    """
    Simulates user assignments and conversion events.

    Args:
        num_users (int): Total users to simulate.
        variants (list): List of variant names.
        conversion_rates (dict): e.g., {"A": 0.1, "B": 0.12}

    Returns:
        DataFrame: user_id, variant, converted
    """
    data = []
    for i in range(num_users):
        user_id = f"user_{i}"
        variant = random.choice(variants)
        converted = int(random.random() < conversion_rates[variant])
        data.append((user_id, variant, converted))
    
    return pd.DataFrame(data, columns=["user_id", "variant", "converted"])
