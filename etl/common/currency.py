# Convert a native-currency amount to USD using the exchange_rates table.
#
# Raises ValueError if no rate is on file - callers should skip/log the
# observation rather than silently inserting an unconverted amount.
def to_usd(cur, amount, currency_code):
    if currency_code == "USD":
        return round(float(amount), 2)

    cur.execute(
        "SELECT usd_per_unit FROM exchange_rates WHERE currency_code = %s",
        (currency_code,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"no exchange rate on file for currency {currency_code!r}")

    usd_per_unit = row["usd_per_unit"] if isinstance(row, dict) else row[0]
    return round(float(amount) * float(usd_per_unit), 2)


# Convert a USD amount to another currency using the exchange_rates
# table - the inverse of to_usd(). Everything is stored internally in USD
# this exists purely for display purposes.
def from_usd(cur, amount_usd, currency_code):
    if currency_code == "USD":
        return round(float(amount_usd), 2)

    cur.execute(
        "SELECT usd_per_unit FROM exchange_rates WHERE currency_code = %s",
        (currency_code,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"no exchange rate on file for currency {currency_code!r}")

    usd_per_unit = row["usd_per_unit"] if isinstance(row, dict) else row[0]
    return round(float(amount_usd) / float(usd_per_unit), 2)
