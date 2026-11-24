from aiogram import Router
from .start import router as start_router
from .account import router as account_router

router = Router()

router.include_routers(start_router, account_router)
