import Levenshtein
import dspy
from typing import Union
import os

import dspy.teleprompt

lm = dspy.LM(
    "openai/VAGOsolutions/SauerkrautLM-Nemo-12b-Instruct-awq",
    cache=False,
    temperature=0,
    api_key=os.getenv("PARROTPARK_API_KEY"),
    base_url="https://api.parrotpark.correlaid.org/v1",
)
dspy.configure(lm=lm)


class OrganizationMatcher(dspy.Signature):
    """Checks if the names of two organizations match"""

    Organization_Name_Input_A: str = dspy.InputField()
    Organization_Name_Input_B: str = dspy.InputField()
    same_org: bool = dspy.OutputField(
        desc="Wether the two version of the organization names refer to the same organization"
    )


matcher = dspy.Predict(OrganizationMatcher)

tp = dspy.teleprompt.LabeledFewShot()

examples = [
    # Different legal entity types
    dspy.Example(
        Organization_Name_Input_A="Tesla, Inc.",
        Organization_Name_Input_B="Tesla Motors",
        same_org=True,
    ).with_inputs("Organization_Name_Input_A", "Organization_Name_Input_B"),
    # Completely different organizations
    dspy.Example(
        Organization_Name_Input_A="Apple Inc.",
        Organization_Name_Input_B="Orange SA",
        same_org=False,
    ).with_inputs("Organization_Name_Input_A", "Organization_Name_Input_B"),
    # Cut-off organization name (same org)
    dspy.Example(
        Organization_Name_Input_A="Johnson & Johnson Pharmaceutical",
        Organization_Name_Input_B="Johnson & Johns",
        same_org=True,
    ).with_inputs("Organization_Name_Input_A", "Organization_Name_Input_B"),
]


opt_prog = tp.compile(student=matcher, trainset=examples)

def norm_lev(a, b):
    """
    Compare two strings and determine if they are similar based on normalized Levenshtein distance.

    Args:
        a (str): First string to compare
        b (str): Second string to compare

    Returns:
        bool: True if strings are similar, False otherwise
    """
    a_ = a.strip()
    b_ = b.strip()

    max_len = max(len(a_), len(b_))
    if max_len == 0:
        return a == b

    edit_distance = Levenshtein.distance(a_, b_)
    return edit_distance / max_len


def match_organisations(a, b, use_llm=False, threshold=0.2, max_threshold=0.4):
    """
    Match organization names considering exact matches and edit distance.

    Args:
        a (str): First organization name
        b (str): Second organization name
        threshold (float): Threshold below which names are considered matching
        max_threshold (float): Threshold above which names are definitely not matching

    Returns:
        bool: True if organizations match, False otherwise
    """
    if a is None or b is None:
        return False

    def rpl(s):
        return s.replace("e.V.", "").replace("(haftungsbeschränkt)", "").lower().strip()

    a_ = rpl(a)
    b_ = rpl(b)
    if a_ == b_:
        return True

    normalized_distance = norm_lev(a,b)

    # If distance is small enough, match without LLM
    if normalized_distance <= threshold:
        return True

    if use_llm:
        # If distance is too large, definitely not a match
        if normalized_distance >= max_threshold:
            return False

        # Only call LLM for ambiguous cases
        return opt_prog(
            Organization_Name_Input_A=a, Organization_Name_Input_B=b
        ).same_org
    else:
        return False
