from .user import router as user_router
from .product import router as product_router
from .category import router as category_router
from .address import router as address_router
from .cart import router as cart_router
from .order import router as order_router
from .payment import router as payment_router
from .refund import router as refund_router
from .role import router as role_router
from .shipping import router as shipping_router
# Add other routers as needed

__all__ = [
    "user_router",
    "product_router",
    "category_router",
    "address_router",
    "cart_router",
    "order_router",
    "payment_router",
    "refund_router",
    "role_router",
    "shipping_router",
] 