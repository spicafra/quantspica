import pytest

def test_torch_import():
    import torch
    assert torch.__version__ is not None

def test_tf_import():
    import tensorflow as tf
    assert tf.__version__ is not None

def test_alpaca_import():
    import alpaca_trade_api as alpaca
    assert hasattr(alpaca, 'REST')
