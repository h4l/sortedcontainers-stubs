from sortedcontainers import SortedDict


def test_sorteddict_types() -> None:
    d = SortedDict[int, str]()
    d[2] = "2"
    d[0] = "0"
    d[4] = "4"
    reveal_type(d[4])
