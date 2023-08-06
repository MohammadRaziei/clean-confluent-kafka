import pytest

from clean_confluent_kafka.utils import flatten_dict, reverse_flatten_dict

pair_dicts = [{"hierarchical": {"key1": {"key11": "val1", "key12": "val2"}, "key2": "val3"},
               "flatted": {"key1.key11": "val1", "key1.key12": "val2", "key2":"val3"}}]


@pytest.mark.parametrize("pair", pair_dicts)
def test_reverse_flatten_dict(pair):
    assert pair["hierarchical"] == reverse_flatten_dict(pair["flatted"])


@pytest.mark.parametrize("pair", pair_dicts)
def test_flatten_dict(pair):
    assert pair["flatted"] == flatten_dict(pair["hierarchical"])



