from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, categories, orders, payments, services, users, vendors

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(vendors.router)
api_router.include_router(categories.router)
api_router.include_router(services.router)
api_router.include_router(orders.router)
api_router.include_router(payments.router)
api_router.include_router(admin.router)
