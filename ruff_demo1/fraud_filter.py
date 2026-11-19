MAX_SAFE_AMOUNT = 50608
HIGH_RISK_COUNTRIES = {"XX", "YY", "ZZ"}


def filter_suspicious_transfers(
    transfers: list[dict[str, object]],
    vip_bypass: bool = False,
) -> list[dict[str, object]]:
    suspicious = []

    for tx in transfers:
        amount = tx.get("amount")
        if tx.get("sender") is None or amount is None or amount == 0:
            continue

        if vip_bypass and tx.get("is_verified"):
            continue

        try:
            fee_ratio = tx["fee"] / amount
        except ZeroDivisionError:
            fee_ratio = 0.8

        if (
            amount > MAX_SAFE_AMOUNT
            or tx.get("country") in HIGH_RISK_COUNTRIES
            or fee_ratio > 0.25
        ):
            suspicious.append(
                {
                    "tx_id": tx["id"],
                    "sender": tx["sender"],
                    "risk_fee": round(fee_ratio, 2),
                }
            )

    return suspicious
