
# Full Node Python Bridge (fnpb)

> | Variable    | Value      | Description                                 |
> | ----------- | ---------- | ------------------------------------------- |
> | FN_HOSTNAME | umbrel.lan | The hostname of the full node.              |
> | FN_USERNAME | umbrel     | The username running bitcoin-cli and lncli. |
> | FN_PASSWORD | ********   | The password of the username.               |

## node

The full node SSH client using **paramiko**.

## ln_info

## ln_invoice

Contains the LNInvoice class that connects to your full node and executes Bitcoin or Lightning Network commands. 

The lightning invoices are fetched from the full node and converted to a **pandas** data frame. 

## type_aliases

## currency_converter

Contains methods to convert between BTC/Sats and USD/GBP/EUR using the <https://api.coindesk.com/v1/bpi/currentprice.json> API.
