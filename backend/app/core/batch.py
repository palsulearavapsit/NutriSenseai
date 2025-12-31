batch = []
MAX_BATCH = 5

def add_to_batch(item):
    batch.append(item)
    if len(batch) >= MAX_BATCH:
        return batch.copy()
    return None
