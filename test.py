from decimal import Decimal
import hashlib
import os
from dotenv import load_dotenv
from ln_invoice import LNInvoice
from ln_info import LNInfo
import currency_converter

load_dotenv()
HOSTNAME = os.getenv("FN_HOSTNAME")
USERNAME = os.getenv("FN_USERNAME")
PASSWORD = os.getenv("FN_PASSWORD")

print("HOSTNAME = ", HOSTNAME)
print("USERNAME = ", USERNAME)
print("PASSWORD = ", PASSWORD)

# 
# a user of a wallet can send or receive
# 
# to receive 
#     what is payment_hash and payment_image
# 

info = LNInfo(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
print(info.get_version())
print(info.get_lightning_address())

print("info.get_block_height()        = ", info.get_block_height())
print("info.get_block_hash()          = ", info.get_block_hash())
print("info.get_best_header_timestamp = ", info.get_best_header_timestamp())

# invoice = LNInvoice(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
# invoice.to_csv()

# print("-" * 80)
# preimage = invoice._df.iloc[0]['r_preimage']
# preimage_hash = invoice._df.iloc[0]['r_hash']
# payment_requests = invoice._df.iloc[0]['payment_request']
# print(f"preimage         = {preimage}")
# print(f"preimage_hash    = {preimage_hash}")
# preimage_sha256 = hashlib.sha256(preimage.encode("utf-8")).hexdigest()
# print(f"sha256(preimage) = {preimage_sha256}")
# sha256(preimage) == payment_hash
# - What are amt_paid, amt_paid_sat, amt_paid_msat?

# print("-" * 80)
# print(invoice.get_created_before("2021-12-28"))
# print(invoice.get_created_after("2021-12-28"))
# print(invoice.get_created_on("2021-12-28"))

# amount_fiat = Decimal(69.00)
# fiat = "USD"
# amount_sats = convert.fiat_to_sats(amount_fiat, fiat)
# print("amount_fiat = ", amount_fiat)
# print("amount_sats = ", amount_sats)
# df = invoice.add(amount_sats=amount_sats, memo=f"Some invoice for {amount_fiat:,} {fiat} = {amount_sats:,} Sats.", expiry_time=120)
# print(df)


print("-" * 80)
# print("invoice.get_sum()", invoice.get_sum())
# print("invoice.get_mean()", invoice.get_mean())
# print("invoice.get_median()", invoice.get_median())
# print("invoice.get_sigma()", invoice.get_sigma())
# print("invoice.get_sigma_mad()", invoice.get_sigma_mad())

# invoice.add_invoice(amount=9991, memo="yo yo yo!", expiry_time=10)
print("-" * 80)
print("-" * 80)
print("-" * 80)
# invoice.set("state", "UNKNOWN")

# from info import Info
# info = Info(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
# print(info._df)
# print(info.get("block_height"))
# 02690451e2c5381af41b94dc0c6efae1b434899418d62efaea67bc55828c8cbab2@457vyb4izpwn55kkalkhdhsa2aj5p2o5wvvhqnaruspame2sf3ymp7ad.onion:9735
# 02690451e2c5381af41b94dc0c6efae1b434899418d62efaea67bc55828c8cbab2@457vyb4izpwn55kkalkhdhsa2aj5p2o5wvvhqnaruspame2sf3ymp7ad.onion:9735
