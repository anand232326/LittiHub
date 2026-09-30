
import hashlib
import json


def generate_idempotency_hash(
    restaurant_id: str,
    delivery_address: str,
    cart_items: list[dict],
) -> str:

    normalized_items = sorted(
        [
            {
                "menu_item_id": item["menu_item_id"],
                "quantity": item["quantity"],
            }
            for item in cart_items
        ],
        key=lambda item: item["menu_item_id"],
    )

    payload = {
        "restaurant_id": restaurant_id,
        "delivery_address": delivery_address,
        "items": normalized_items,
    }

    serialized_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        serialized_payload.encode("utf-8")
    ).hexdigest()

