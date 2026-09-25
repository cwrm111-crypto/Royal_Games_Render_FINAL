import tempfile, os
def test_imports():
    from backend.services.wallet import WalletService
    assert WalletService
