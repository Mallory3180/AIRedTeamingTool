from src.core.detector import DetectorInput, DetectorOutput


def test_detector_schema_roundtrip():
    inp = DetectorInput(prompt="p", response="r")
    out = DetectorOutput(verdict="allow", scores=[0.1, 0.2])
    assert inp.prompt == "p"
    assert out.verdict == "allow"
