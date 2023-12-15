from src.utils import extract_version_string


class TestExtractVersion:
    def test_v_prefix_version(self):
        assert extract_version_string("v1.2.3-alpha") == "v1.2.3"
        assert extract_version_string("v2.5.7") == "v2.5.7"
        assert extract_version_string("v0.0.0") == "v0.0.0"
        assert extract_version_string("v999.888.777") == "v999.888.777"

    def test_no_v_prefix_version(self):
        assert extract_version_string("1.2.3-alpha4") == "1.2.3"
        assert extract_version_string("some text 1.2.3-alpha4 and more") == "1.2.3"
        assert extract_version_string("some text 1.2.3 and more") == "1.2.3"
        assert extract_version_string("2.5.7") == "2.5.7"
        assert extract_version_string("0.0.0") == "0.0.0"
        assert extract_version_string("11.22.33-beta") == "11.22.33"
        assert extract_version_string("11.22.33-alpha") == "11.22.33"
        assert extract_version_string("11.22.33-rc1") == "11.22.33"

    def test_no_version(self):
        assert extract_version_string("no version here") is None
