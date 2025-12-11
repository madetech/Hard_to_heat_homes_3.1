from src.council_data_utils import load_uprn_to_council
import pytest

@pytest.mark.parametrize(
        "uprn, expected_council_code",
        [
            ("100061342030", "E07000207"),
            ("100061342031", "E07000207"),
            ("10033322698", "E07000207"),
            ("10015441587","E06000023")
        ]
)
def test_load_uprn_to_council_returns_correct_for_valid_uprn(uprn, expected_council_code):
    uprn_to_council_dict = load_uprn_to_council(expected_council_code)
    assert uprn_to_council_dict.get(uprn) == expected_council_code


def test_load_uprn_to_council_has_no_empty_or_none_keys():
    uprn_to_council_dict = load_uprn_to_council("E06000023")
    assert None not in uprn_to_council_dict
    assert "" not in uprn_to_council_dict