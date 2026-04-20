from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.api.depends.auth import UserVerifyDep
from app.api.depends.service import OllamaConversationServiceDep


class AskRequest(BaseModel):
    """
    Solicitud para consultar o controlar dispositivos mediante Ollama
    """

    question: str


class AskResponse(BaseModel):
    """
    Respuesta del asistente inteligente
    """

    response: str


router = APIRouter(tags=["Chat AI"])


@router.post("/ask", response_model=AskResponse)
async def ask_ollama(
    request: AskRequest,
    current_user: UserVerifyDep,
    ollama_service: OllamaConversationServiceDep,
) -> AskResponse:
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
        if current_user.id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        response = ollama_service.chat(
            user_message=request.question,
            user_id=current_user.id,
        )

        return AskResponse(
            response="".join(list(response)),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando la solicitud: {str(e)}",
        )
