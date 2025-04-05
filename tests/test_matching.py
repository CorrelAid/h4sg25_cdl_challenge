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
    # Test cases for threshold 0.3
    # Should be similar (normalized distance < 0.3)
    assert norm_lev("Microsoft Corporation", "Microsoft Corp.") < 0.3
    assert norm_lev("Apple Inc.", "Apple Inc") < 0.3
    assert norm_lev("Google LLC", "Google, LLC") < 0.3
    assert norm_lev("Amazon.com", "Amazon") < 0.3
    assert norm_lev("IBM", "International Business Machines") >= 0.3  # Should be different

    # Test cases for threshold 0.5
    # Should be similar (normalized distance < 0.5)
    assert norm_lev("Microsoft Corporation", "Microsoft") < 0.5
    assert norm_lev("Coca-Cola Company", "Coca Cola Co.") < 0.5
    assert norm_lev("Johnson & Johnson", "Johnson and Johnson") < 0.5
    assert norm_lev("Procter & Gamble", "Procter and Gamble") < 0.5
    assert norm_lev("McDonald's Corporation", "McDonalds Corp") < 0.5

    # Should be different (normalized distance >= 0.5)
    assert norm_lev("Microsoft Corporation", "Apple Inc.") >= 0.5
    assert norm_lev("Walmart", "Target Corporation") >= 0.5
    assert norm_lev("Facebook, Inc.", "Meta Platforms") >= 0.5

    # Edge cases
    assert norm_lev("IBM", "IBM ") < 0.3  # Whitespace should be stripped
    assert norm_lev("", "") == True  # Empty strings

    print("All tests passed!")

# Run the tests
test_norm_lev_thresholds()
