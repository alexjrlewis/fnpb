
# Full Node Python Bridge (fnpb)

> | Variable    | Value      | Description
> | ----------- | ---------- | ------------------------------------------- |
> | FN_HOSTNAME | umbrel.lan | The hostname of the full node.              |
> | FN_USERNAME | umbrel     | The username running btc-cli and lncli.     |
> | FN_PASSWORD | ********   | The password of the username.               |

## ln_invoice

Contains the LNInvoice class that connects to your full node and executes Lightning Network commands to query its invoices. 

## currency_converter

Contains methods to convert between BTC/Sats and USD/GBP/EUR using the <https://api.coindesk.com/v1/bpi/currentprice.json> API.
