
# Full Node Python Bridge (fnpb)

This software provides a Python wrapper/bridge by executing RPCs to your full node.

## Installation

..

## fnpb.node

Contains the *Node* class that provides an SSH client, which connects to the full node using **paramiko**. This class expects the following variables:

  | Variable | Example Value      | Description                                 |  
  | -------- | ------------------ | ------------------------------------------- |  
  | hostname | umbrel.lan         | The hostname of the full node.              |  
  | username | umbrel             | The username running bitcoin-cli and lncli. |  
  | password | moneyprintergobrrr | The password of the username.               |  


### exec_btc_command

Executes a bitcoin-cli command and returns the result as a Python dictionary.

### exec_ln_command

Executes a lncli command and returns the result as a Python dictionary.

## fnpb.ln

### .info

Contains the *Info* class that provides a summary of the LN daemon that the connected node is running.

### invoice

Contains the *Invoice* class that handles your Lightning invoices. This class connects to your full node and fetches all of your full node's lightning invoices as represents them as a pandas data frame. This data frame is then used to query and perform statistics on the invoices.

### get

Executes the **listinvoices** command on the node and casts/returns the **invoices** value as a pandas data frame.

### get_with_state
  foo bar

### get_created_after
  foo bar

### get_created_before
  foo bar

### get_created_on
  foo bar

### get_first
  foo bar

### get_last
  foo bar

### get_query
  foo bar

## fnpb.utils.type_aliases

Contains useful type aliases, e.g. Bitcoin and Satoshi as aliases for decimal.Decimal objects suitable for currency computations.

## fnpb.utils.currency_converter

Contains methods to convert between BTC/Sats and USD/GBP/EUR using the <https://api.coindesk.com/v1/bpi/currentprice.json> API.
