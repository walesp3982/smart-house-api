import asyncio
import secrets

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from app.api.depends.auth import UserVerifyDep
from app.api.depends.service import StateDeviceServiceDep
from app.exceptions.command_exception import StateNotFoundDeviceError

router = APIRouter()

ws_tickets: dict[str, int] = {}


async def expire_ticket(ticket: str, seconds: int):
    await asyncio.sleep(seconds)
    ws_tickets.pop(ticket, None)


class TicketSocket(BaseModel):
    ticket: str


@router.post("/auth/ws-ticket")
async def get_ws_ticket(user: UserVerifyDep) -> TicketSocket:
    ticket = secrets.token_urlsafe(32)
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id del usuario no encontrado",
        )
    ws_tickets[ticket] = user.id
    asyncio.create_task(expire_ticket(ticket, 30))
    return TicketSocket(ticket=ticket)


@router.websocket("/ws/{installed_device_id}")
async def state_device(
    websocket: WebSocket,
    installed_device_id: int,
    state_device_service: StateDeviceServiceDep,
    ticket: str = Query(...),
):
    user_id = ws_tickets.pop(ticket, None)
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    try:
        while True:
            try:
                (is_online, state) = await run_in_threadpool(
                    state_device_service.execute, user_id, installed_device_id
                )
                json_state = state.model_dump(mode="json")
                json_state["status"] = "online" if is_online else "offline"
                await websocket.send_json(json_state)
                await asyncio.sleep(0.5)

            except StateNotFoundDeviceError:
                await websocket.send_json(
                    {
                        "status": "waiting",
                        "message": "Dispositivo no conectado",
                    }
                )
    except WebSocketDisconnect:
        pass
