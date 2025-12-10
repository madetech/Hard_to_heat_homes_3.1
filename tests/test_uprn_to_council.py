# from src.council_data_utils import get_council_code_for_uprn
# import pytest

# @pytest.mark.parametrize(
#         "uprn, expected_council_code",
#         [
#             ("100061342030", "E07000207"),
#             ("100061342031", "E07000207"),
#             ("10033322698", "E07000207")
#         ]
# )
# def test_get_council_code_for_uprn_returns_correct_for_valid_uprn(uprn, expected_council_code):
#     council_code = get_council_code_for_uprn(uprn)
#     assert council_code == expected_council_code

# def test_get_council_code_for_uprn_returns_None_for_invalid_uprn():
#     uprn = "this is not a uprn"

#     council_code = get_council_code_for_uprn(uprn)
#     assert council_code is None

# def test_get_council_code_for_uprn_returns_false_for_None():
#     uprn = None

#     council_code = get_council_code_for_uprn(uprn)
#     assert council_code is None