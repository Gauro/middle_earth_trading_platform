# main.py
import uvicorn
from fastapi import FastAPI

from middle_earth_trading_platform.routes import user_routes, offer_routes

# Create FastAPI app
app = FastAPI()

# Include user routes
app.include_router(user_routes.router, tags=["User"])

# Include offer routes
app.include_router(offer_routes.router, tags=["Offers"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
