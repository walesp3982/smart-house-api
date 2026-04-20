from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api.depends.auth import UserVerifyDep
from app.api.depends.service import OllamaConversationServiceDep


class AskRequest(BaseModel):
    """
    Solicitud para consultar o controlar dispositivos mediante Ollama
    """

    question: str


router = APIRouter(tags=["Chat AI"])


@router.post("/ask")
def ask_ollama(
    request: AskRequest,
    current_user: UserVerifyDep,
    ollama_service: OllamaConversationServiceDep,
) -> StreamingResponse:
    """
    Procesa preguntas y órdenes de voz mediante Ollama

    Ejemplos:
    - "¿Cuántas luces están prendidas?" → Consulta estado y responde
    - "Apaga todas las luces" → Ejecuta el comando
    - "¿Cuál es la temperatura?" → Consulta termostatos

    Args:
        request: Pregunta u orden del usuario
        current_user: Usuario autenticado
        ollama_service: Servicio de integración con Ollama

    Returns:
        AskResponse con la respuesta natural y el historial de conversación
    """
    try:

        def generate():
            if current_user.id is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            for token in ollama_service.chat(
                user_message=request.question,
                user_id=current_user.id,
            ):
                yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando la solicitud: {str(e)}",
        )
