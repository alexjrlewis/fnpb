
from decimal import Decimal
from typing import Annotated

MilliSatoshi = Annotated[Decimal, "mSat"]
Satoshi = Annotated[Decimal, "Sat"]
Bitcoin = Annotated[Decimal, "BTC"]
Fiat = Annotated[Decimal, "Fiat"]
Second = Annotated[int, "second"]
