# ab_core/assign.py

import hashlib

def assign_user(user_id, experiment_name, variants):
    """
    Assigns a user to one of the variants deterministically based on hash.
    """
    key = f"{user_id}_{experiment_name}"
    hash_val = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    index = hash_val % len(variants)
    return variants[index]
