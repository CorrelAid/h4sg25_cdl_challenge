from helpers import match_organisations

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
        ("ABC", "ABCDEF", False)  # Too different
    ]

    # Run tests
    for org1, org2, expected in test_cases:
        result = match_organisations(org1, org2)
        print(f"'{org1}' and '{org2}': Expected {expected}, Got {result}")
        assert result == expected, f"Failed: '{org1}' and '{org2}'"

    print("All tests passed!")

# Run the tests
test_match_organisations()
