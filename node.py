"""Module containing the Node class."""

import json
import os
from typing import Dict, Optional
import paramiko


class Node:
    """Class providing a connection to an SSH client representing a node.

    Attributes:
        hostname: The hostname of the node.
        username: The username of the node.
        password: The password of the node.
        is_docker: Is the node running bitcoin/lightning on docker?
        ssh_client: A connected SSH client.
    """

    def __init__(self, hostname: str, username: str, password: str, is_docker: bool = True):
        """Initializes a new instance."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.is_docker = is_docker
        self.ssh_client = self._get_ssh_client()

    def _get_ssh_client(self) -> paramiko.client.SSHClient:
        """Returns a connection to an SSH client

        Returns:
            An SSH connection given the above credentials.
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.hostname, username=self.username, password=self.password)
        return ssh_client

    def _exec_command(self, cli_command: str, command: str) -> Optional[Dict[str, str]]:
        """Executes bitcoin or lighting command on the SSH client.

        Args:
            command: The command to execute, which must return valid JSON response.
                https://stackoverflow.com/questions/39491420/python-jsonexpecting-property-name-enclosed-in-double-quotes
            layer: The layer, bitcoin or lightning (default).
        Returns:
            A JSOn response of the bitcoin or lightning command or None.
        """
        command = f"{cli_command} {command}"
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        stdin.close()
        s = "".join(stdout.readlines())
        s = s.strip()
        s = s.replace("\'", "\"")
        data = json.loads(s)
        return data

    def exec_btc_command(self, command: str) -> Dict[str, str]:
        """Executes a bitcoin command.

        Args:
            command: The bitcoin command to execute.
        Returns:
            A JSON response from the bitcoin command.
        """
        if self.is_docker:
            return self._exec_command(f"docker exec bitcoin bitcoin-cli", command)
        else:
            return self._exec_command(f"{self.username}/bin/bitcoin-cli", command)

    def exec_ln_command(self, command: str) -> Dict[str, str]:
        """Executes a lightning command.

        Args:
            command: The lightning command to execute.
        Returns:
            A JSON response from the lightning command.
        """
        if self.is_docker:
            return self._exec_command("docker exec lnd lncli", command)
        else:
            return self._exec_command(f"{self.username}/bin/lncli", command)
