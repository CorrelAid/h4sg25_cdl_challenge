from helpers import match_organisations, norm_lev

def test_match_organisations():
    """Test the match_organisations function with various cases."""
    # Test cases from the provided lists
    test_cases = [
        # Should match (same organization with slight differences)
        ("Correl aid", "CorrelAid", True),
        ("CorrelAid", "CorrelAid e.V.", True), # e.V. missing
        ("Caritas", "Karitas", True),
        ("Greenpeace", "Greenpeace", True),

        # Additional test cases
        # Exact matches
        ("UNICEF", "UNICEF", True),

        # Case differences
        ("red cross", "Red Cross", True),
        ("WWF", "wwf", True),

        # Small edit distances
        ("Médecins Sans Frontières", "Medecins Sans Frontieres", True),

        # Should not match (different organizations)
        ("Amnesty International", "Human Rights Watch", False),
        ("Save the Children", "Children International", False),
        ("CARE", "SHARE", False),

        # Edge cases
        ("", "", True),
        ("A", "a", True),
        ("ABC", "ABCDEF", False), # Too different

        # Cut off Names
        ("Zentrum für Kunst und Medien Karlsruhe", "Zentrum für Kunst und Medien Karlsr", True)
    ]

    # Run tests
    for org1, org2, expected in test_cases:
        result = match_organisations(org1, org2)
        print(f"'{org1}' and '{org2}': Expected {expected}, Got {result}")
        assert result == expected, f"Failed: '{org1}' and '{org2}'"

    print("All tests passed!")

def test_norm_lev_thresholds():
    # Test cases for threshold 0.2
    min_t = 0.2
    assert norm_lev("Microsoft Corporation", "Microsoft Corp.") > min_t
    assert norm_lev("Apple Inc.", "Apple Inc") < min_t
    assert norm_lev("Google LLC", "Google, LLC") < min_t

    assert norm_lev("Amazon.com", "Amazon") >= min_t  # Should be different
    assert norm_lev("IBM", "International Business Machines") >= min_t  # Should be different

    max_t = 0.5

    assert norm_lev("Coca-Cola Company", "Coca Cola Co.") < max_t
    assert norm_lev("Johnson & Johnson", "Johnson and Johnson") < max_t
    assert norm_lev("Procter & Gamble", "Procter and Gamble") < max_t
    assert norm_lev("McDonald's Corporation", "McDonalds Corp") < max_t

    # Should be different (normalized distance >= 0.5)
    assert norm_lev("Microsoft Corporation", "Microsoft") > max_t
    assert norm_lev("Microsoft Corporation", "Apple Inc.") >= max_t
    assert norm_lev("Walmart", "Target Corporation") >= max_t
    assert norm_lev("Facebook, Inc.", "Meta Platforms") >= max_t

    print("All tests passed!")

# Run the tests
test_norm_lev_thresholds()
