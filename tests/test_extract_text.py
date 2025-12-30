from smelter.extract_text import parse_pages

def test_parse_pages():
    assert parse_pages("1-3", 10) == [0, 1, 2]
    assert parse_pages("2,4,6", 10) == [1, 3, 5]
    assert parse_pages("1-3,5", 5) == [0, 1, 2, 4]
