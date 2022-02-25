
# Full Node Python Bridge (fnpb)

This software provides a Python wrapper/bridge to your full node.

## fnpb.node

Contains the *Node* class that provides an SSH client, which connects to the full node using **paramiko**. This class expects the following variables:

  | Variable | Example Value      | Description                                 |  
  | -------- | ------------------ | ------------------------------------------- |  
  | hostname | umbrel.lan         | The hostname of the full node.              |  
  | username | umbrel             | The username running bitcoin-cli and lncli. |  
  | password | moneyprintergobrrr | The password of the username.               |  


## fnpb.ln.info

Contains the *Info* class that provides a summary of the LN daemon that the connected node is running.

## fnpb.ln.invoice

Contains the *Invoice* class that connects to your full node and executes Bitcoin or Lightning Network commands. The lightning invoices are fetched from the full node and converted to a pandas data frame. 

## fnpb.utils.type_aliases

Contains useful type aliases, e.g. Bitcoin and Satoshi as aliases for decimal.Decimal objects suitable for currency computations.

## fnpb.utils.currency_converter

Contains methods to convert between BTC/Sats and USD/GBP/EUR using the <https://api.coindesk.com/v1/bpi/currentprice.json> API.
