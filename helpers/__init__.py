import Levenshtein

def match_organisations(a, b, threshold=0.3):
    """
    Match organization names considering exact matches and edit distance.

    Args:
        a (str): First organization name
        b (str): Second organization name

    Returns:
        bool: True if organizations match, False otherwise
    """
    if a.lower() == b.lower():
        return True
    def rpl(s):
            return s.replace("e.V.", "").replace("(haftungsbeschränkt)", "")
    
    # remove e.V. etc.
    a = rpl(a)
    b = rpl(b)

    # Edit distance-based match
    # Calculate normalized edit distance (0-1 scale)
    max_len = max(len(a), len(b))

    edit_distance = Levenshtein.distance(a.lower(), b.lower())
    normalized_distance = edit_distance / max_len

    # Consider a match if normalized distance is below threshold
    # Threshold can be adjusted based on requirements
    return normalized_distance <= threshold  # 30% difference threshold