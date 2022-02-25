"""Module containing the LNInfo class to return basic information related to the active daemon."""

import json
import os
from typing import Dict, Optional
import pandas as pd
from fnpb.node import Node

COLUMN_TO_DTYPE = {
    "version": str,
    "commit_hash": str,
    "identity_pubkey": str,
    "alias": str,
    "color": str,
    "num_pending_channels": str,
    "num_active_channels": str,
    "num_inactive_channels": str,
    "num_peers": str,
    "block_height": str,
    "block_hash": str,
    "best_header_timestamp": int,
    "synced_to_chain": str,
    "synced_to_graph": str,
    "testnet": str,
    "chains": str,
    "uris": list,
    "features": str,
}


class Info(Node):
    """A Lightning Network information class."""

    def __init__(self, **kwargs):
        """Initialize a new instance."""
        super().__init__(**kwargs)
        self._df = self.get_df()

    def _get_data(self) -> Dict[str, str]:
        """

        Returns:
        """
        command = f"getinfo"
        data = self.exec_ln_command(command)
        return data

    def get_df(self) -> pd.DataFrame:
        """

        Returns:
        """
        data = self._get_data()
        for column, dtype in COLUMN_TO_DTYPE.items():
            data[column] = dtype(data[column])
        df = pd.DataFrame(data, index=[0])
        df["best_header_timestamp"] = pd.to_datetime(
            df["best_header_timestamp"], unit="s"
        )  # cast to readable date format.
        return df

    def get_block_height(self) -> int:
        """."""
        return self._df["block_height"][0]

    def get_block_hash(self) -> int:
        """."""
        return self._df["block_hash"][0]

    def get_best_header_timestamp(self) -> int:
        """."""
        return self._df["best_header_timestamp"][0]

    def get_alias(self) -> str:
        """Returns"""
        return self._df["alias"][0]

    def get_version(self) -> str:
        """Returns"""
        return self._df["version"][0]

    def get_lightning_address(self) -> str:
        """Other Lightning nodes can open payment channels to your node on the following address."""
        return self._df["uris"][0]
