"""Module containing the Invoice class that acts as a DAO to the invoices stored on the node."""

from typing import Any, Dict, List, Optional
import pandas as pd

from node import Node
from type_aliases import Satoshi, MilliSatoshi, Second

MEMO_MAX_BYTES = 639  # https://bitcoin.stackexchange.com/questions/85951/whats-the-maximum-size-of-the-memo-in-a-ln-payment-request
STATES = ["OPEN", "SETTLED", "CANCELED", "ACCEPTED", "UNKNOWN"]
COLUMN_TO_DTYPE = {
    "memo": str,
    "r_preimage": str,
    "r_hash": str,
    "value": Satoshi,
    "value_msat": MilliSatoshi,
    "settled": bool,
    "creation_date": Second,
    "settle_date": Second,
    "payment_request": str,
    "description_hash": str,
    "expiry": int,
    "fallback_addr": str,  # on-chain Bitcoin address in case.
    "cltv_expiry": int,
    "route_hints": str,
    "private": bool,
    "add_index": int,
    "settle_index": int,
    "amt_paid": Satoshi,
    "amt_paid_sat": Satoshi,
    "amt_paid_msat": MilliSatoshi,
    "state": str,
    "htlcs": str,
    "features": str,
    "is_keysend": bool,
    "payment_addr": str,
    "is_amp": bool,
    "amp_invoice_state": str,
}


def clip_memo(memo: str) -> str:
    """Clips the memo such that it is within the MEMO_MAX_BYTES size.

    Args:
        memo: The memo to clip.
    Returns:
        The clipped memo such that its size is less than the MEMO_MAX_BYTES.
    """
    if len(memo.encode("utf-8")) > MEMO_MAX_BYTES:
        _memo = ""
        for i, c in enumerate(memo):
            if len((_memo + c).encode("utf-8")) < MEMO_MAX_BYTES:
                _memo += c
        return _memo
    return memo


class LNInvoice(Node):
    """A Lightning Network invoice class."""

    def __init__(self, **kwargs):
        """Initialize a new instance."""
        super().__init__(**kwargs)
        self._df = self.get_df()

    def _get_data(self) -> Dict[str, str]:
        """Queries the lightning node and returns a list of all invoices ever created. For
        recording keeping, invoices are never deleted but instead their status is kept track
        of. The data is in JSON format at the first element of the array is "invoices"

        Returns:
            A dictionary containing all invoices on the node as an array under the
            first key "invoices".
        """
        data = self.exec_ln_command("listinvoices")
        return data

    def get_df(self) -> pd.DataFrame:
        """Fetches the invoice data on the lightning node as a JSON dictionary and returns
        it as a pandas data frame.

        Returns:
            A pandas data frame containing all invoices on the node.
        """
        data = self._get_data()
        data = data["invoices"]
        _data = []  # data cast to specified types.
        for d in data:
            for column, dtype in COLUMN_TO_DTYPE.items():
                d[column] = dtype(d[column])
            _data.append(d)
        df = pd.DataFrame(_data)
        df["state"] = df["state"].apply(lambda s: str(s).upper())
        df["creation_date"] = pd.to_datetime(
            df["creation_date"], unit="s"
        )  # cast to readable date format.
        df["settle_date"] = pd.to_datetime(df["settle_date"], unit="s")
        return df

    def get_compressed_df(self) -> pd.DataFrame:
        """Returns a data frame with only a selection of invoice columns.

        Returns:
            The data frame with only a selection of columns.
        """
        columns = ["memo", "value", "creation_date", "payment_request"]
        df = self._df[columns].copy()
        return df

    def get_sum(self, query: Optional[str] = None) -> Satoshi:
        """Returns the sum of the values of the invoices.

        Args:
            query: Filter by an optional query.
        Returns:
            The sum value of the invoices.
        """
        value = self.get_query(query)["value"].sum()
        return value

    def get_mean(self, query: Optional[str] = None) -> Satoshi:
        """Returns the mean of the values of the invoices.

        Args:
            query: Filter by an optional query.
        Returns:
            The mean value of the invoices.
        """
        value = self.get_query(query)["value"].mean()
        return value

    def get_median(self, query: Optional[str] = None) -> Satoshi:
        """Returns the median of the values of the invoices.

        Args:
            query: Filter by an optional query.
        Returns:
            The median value of the invoices.
        """
        value = self.get_query(query)["value"].median()
        return value

    def get_sigma(self, query: Optional[str] = None) -> Satoshi:
        """Returns the standard deviation of the value of the invoices.

        Args:
            query: Filter by an optional query.
        Returns:
            The standard deviation of the the values of the invoices.
        """
        # value = self.get_query(query)["value"].apply()
        # return value
        pass

    def get_sigma_mad(self, query: Optional[str] = None) -> Satoshi:
        """Returns the MAD sigma estimator of the value of the invoices.

        Args:
            query: Filter by an optional query.
        Returns:
            The MAD sigma of the value of the invoices.
        """
        # value = self.get_query(query)["value"].apply()
        # return value
        pass

    def get_number_of_invoices(self, query: Optional[str] = None) -> int:
        """Returns the number of invoices.

        Args:
            query: Filter by an optional query.
        Returns:
            The number of invoices.
        """
        return len(self.get_query(query))

    def get_with_state(self, state: str = "UNKNOWN") -> pd.DataFrame:
        """Returns the invoices with a given state.

        Args:
            state: The state that the invoices should have.
        Returns:
            All invoices with a given state.
        """
        if state in STATES:
            return self.get_query(f"state == \"{state.upper()}\"").copy()
        return self._df.copy()

    def get_created_after(self, creation_date: str) -> pd.DataFrame:
        """Gets all invoices created after a certain date.

        Args:
            creation_date: The date invoices should be created after.
        Returns:
            The invoices created after a given date.
        """
        return self._df[self._df["creation_date"] > creation_date].copy()

    def get_created_before(self, creation_date: str) -> pd.DataFrame:
        """Gets all invoices created before a certain date.

        Args:
            creation_date: The date invoices should be created before.
        Returns:
            The invoices created before a given date.
        """
        return self._df[self._df["creation_date"] < creation_date].copy()

    def get_created_on(self, creation_date: str) -> pd.DataFrame:
        """Gets all invoices created on a certain date.

        Args:
            creation_date: The date invoices should be created on.
        Returns:
            The invoices created on a given date.
        """
        return self._df[self._df["creation_date"] == creation_date].copy()

    def get_settled(self) -> pd.DataFrame:
        """Returns invoices that are settled.

        Returns:
            The invoices that are settled.
        """
        return self._df.copy()[self._df["settled"]]

    def get_fist(self) -> pd.DataFrame:
        """Gets and returns the first invoice.

        Returns:
            Returns the first invoice as a data frame.
        """
        return self._df.iloc[[0]].copy()

    def get_last(self) -> pd.DataFrame:
        """Gets and returns the latest invoice.

        Returns:
            Returns the latest invoice as a data frame.
        """
        return self._df.iloc[[-1]].copy()

    def get_query(self, query: Optional[str] = None) -> pd.DataFrame:
        """Queries the data frame of invoices and returns that data frame.

        Args:
            query: The query string to query the data frame with.
        Returns:
            The queried data frame.
        """
        if query is not None:
            return self._df.query(query)
        return self._df

    def get_indices(query: str) -> Optional[List[int]]:
        """Gets and returns the indices of a given query.

        Args:
            query: The query to return the indices for
        Returns:
            An optional list of integer indices.
        """
        df = self._df.query(query)
        indices = df_.index.tolist()
        if len(indices):
            return indices

    def get_first_index(query: str) -> Optional[int]:
        """Gets and returns the first integer index of a data frame given a query.

        Args:
            query: The query string to query the data frame with.
        Returns:
            The first index of the queried invoices data frame.
        """
        try:
            indices = self.get_indices(query)
            index = indices[0]
        except:
            pass
        else:
            return index

    def add(self, amount_sats: Satoshi, memo: str = "", expiry_time: Second = 86400) -> pd.DataFrame:
        """Adds and returns a lightning invoice. The input parameters are filtered.

        Args:
            amount_sats: The amount in satoshis of the invoice.
            memo: The memo, i.e. description, of the invoice.
            expiry_time: How long the invoice lasts, in seconds (default is a day).
        """
        amount_msat = round(amount_sats * Satoshi(1e3))  # convert satoshi amount to milli satoshis.
        command = f'addinvoice --amt_msat {amount_msat} --memo "{clip_memo(memo)}" --expiry {expiry_time}'
        data = self.exec_ln_command(command)
        df = pd.DataFrame(data, index=[0])
        return df

    def pay(self):
        """Pays a lightning invoice.

        Args:
            amount: The amount in satoshis of the invoice.
        """
        # command = ""
        # self.exec_ln_command(command)
        pass

    def cancel_at_index(self, index: int):
        """Cancels an invoice at a given index. You can only cancel

        Args:
            index: Cancels the invoice at this index.
        """
        # row = self._df.iloc[index]
        # r_hash = row["r_hash"]
        # command = f'cancelinvoice --paymenthash "{r_hash}"'
        # self.exec_ln_command(command)
        pass

    def to_csv(self, filename="data/ln_invoice.csv"):
        """
        """
        self._df.to_csv(filename, index=False)

