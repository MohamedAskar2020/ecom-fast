import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app import models, database
from app.auth import router as auth_router
from app.routers import user_router, product_router, category_router, address_router, cart_router, order_router, payment_router, refund_router, role_router, shipping_router  # Import the shipping router
from app.config import UPLOAD_DIRECTORY  # Import from config
from fastapi.responses import FileResponse

# Create the FastAPI app with lifespan context manager
app = FastAPI()

# Allow CORS for all origins (adjust as necessary for your use case)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])  # Include the user router
app.include_router(product_router, prefix="/products", tags=["products"])  # Include the product router
app.include_router(category_router, prefix="/categories", tags=["categories"])  # Include the category router
app.include_router(address_router, prefix="/addresses", tags=["addresses"])  # Include the address router
app.include_router(cart_router, prefix="/carts", tags=["carts"])  # Include the cart router
app.include_router(order_router, prefix="/orders", tags=["orders"])  # Include the order router
app.include_router(payment_router, prefix="/payments", tags=["payments"])  # Include the payment router
app.include_router(refund_router, prefix="/refunds", tags=["refunds"])  # Include the refund router
app.include_router(role_router, prefix="/roles", tags=["roles"])  # Include the role router
app.include_router(shipping_router, prefix="/shippings", tags=["shippings"])  # Include the shipping router

# Lifespan context manager
@app.on_event("startup")
async def startup_event():
    # Create the database tables
    database.Base.metadata.create_all(bind=database.engine)

@app.on_event("shutdown")
async def shutdown_event():
    database.SessionLocal().close()


# Define lifespan context manager
async def lifespan(app: FastAPI):
    # Startup actions
    database.Base.metadata.create_all(bind=database.engine)
    yield  # This will pause here and wait for the application to shut down
    # Shutdown actions
    database.SessionLocal().close()

# Attach the lifespan context manager to the app
app.lifespan = lifespan

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API!"}

@app.get("/images/products/{filename}")
async def get_product_image(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    return FileResponse(file_path)

@app.get("/images/categories/{filename}")
async def get_category_image(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    return FileResponse(file_path)
