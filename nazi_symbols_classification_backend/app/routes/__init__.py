"""The main APIRouter is defined to include all the sub routers from each
module inside the api folder"""

from fastapi import APIRouter
from .system import system_router
# TODO: import your modules here.
from .classification import classification_router

router = APIRouter()
router.include_router(system_router, tags=["base"])
router.include_router(classification_router, tags=["classification"])
# TODO: include the routers from other modules
