
# Full Node Python Bridge (fnpb)

This software provides a Python wrapper/bridge to your full node.

  | Variable    | Value      | Description                                 |  
  | ----------- | ---------- | ------------------------------------------- |  
  | FN_HOSTNAME | umbrel.lan | The hostname of the full node.              |  
  | FN_USERNAME | umbrel     | The username running bitcoin-cli and lncli. |  
  | FN_PASSWORD | ********   | The password of the username.               |  

## node.py

Contains the Node class that provides an SSH client, which connects to the full node using **paramiko**.

## ln/info.py

Contains the Info class that provides a summary of the LN daemon that the connected node is running.

## ln/invoice.py

Contains the Invoice class that connects to your full node and executes Bitcoin or Lightning Network commands. The lightning invoices are fetched from the full node and converted to a **pandas** data frame. 

## utils/type_aliases.py

Contains useful type aliases, e.g. Bitcoin and Satoshi as aliases for decimal.Decimal objects suitable for currency computations.

## utils/currency_converter.py

Contains methods to convert between BTC/Sats and USD/GBP/EUR using the <https://api.coindesk.com/v1/bpi/currentprice.json> API.
