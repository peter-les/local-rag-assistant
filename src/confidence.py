from config import MAX_DISTANCE


def has_enough_confidence(results):

    """
    True = we can call LLM

    False = results are too wrong
    """

    if len(results) == 0:

        return False

    best = min(r.distance for r in results)

    return best <= MAX_DISTANCE