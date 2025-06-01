from sqlalchemy import Enum

order_status_enum = Enum(
    "CREATED", "FILLED", "PARTIALLY_FILLED", "CANCELED",
    name="order_status"
)

order_direction_enum = Enum(
    "BUY", "SELL",
    name="order_direction"
)