from bot.dispatcher import dp
from bot.handlers.main import main_router
from bot.handlers.admin import admin_router
from bot.handlers.order import order_router


dp.include_routers(*[
    main_router,
    admin_router,
    order_router
])