from dataclasses import dataclass
import typing

keyset = typing.NamedTuple('Keyset', [
    ('public', str),
    ('private', str),
    ('passphrase', str)])


@dataclass()
class CoinbaseKeys:
    # ==== test key 1 for live account ======
    # DormDevKey1
    live_test = keyset(public='insert key here',
                       private='insert key here',
                       passphrase='insert password here')
    # =======================================

    # ==== live key for live account ======
    prod = keyset(public='===',
                  private='===',
                  passphrase='===')
    # =====================================

    # ==== master key for sandbox account =====
    sandbox = keyset(public='===',
                     private='===',
                     passphrase='===')
    # =========================================
