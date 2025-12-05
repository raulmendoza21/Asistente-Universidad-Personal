from typing import List, Dict, Callable, Any
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from huggingface_hub import InferenceClient
from config import HF_TOKEN, MODEL_NAME, SYSTEM_PROMPT, TIMEZONE


class QwenAgent:
    """
    Agente conversacional usando Qwen2.5-72B-Instruct con tool calling
    sobre la Inference API de Hugging Face.
    """

    def __init__(self):
        self.client = InferenceClient(
            model=MODEL_NAME,
            token=HF_TOKEN
        )
        self.conversation_history: List[Dict] = []
        self.tools_map: Dict[str, Any] = {}
        self.tools_schema: List[Dict] = []

    def register_tool(self, name: str, function: callable, description: str, parameters: Dict):
        """
        Registra una herramienta disponible para el agente.

        Args:
            name: Nombre de la herramienta.
            function: Función ejecutable.
            description: Descripción de la herramienta.
            parameters: Schema de parámetros en formato JSON Schema.
        """
        self.tools_map[name] = function

        # Formato compatible con tool calling de Qwen/HF
        self.tools_schema.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        })

    def _build_messages(self, user_message: str = None) -> List[Dict]:
        """
        Construye la lista de mensajes que se envían al modelo,
        usando hora actual y manejando cualquier problema de zona horaria.
        """
        # Manejo robusto de zona horaria
        try:
            ahora = datetime.now(ZoneInfo(TIMEZONE))
        except Exception:
            # Si la zona no existe en el sistema, usa hora local sin zona
            ahora = datetime.now()

        ahora_str = ahora.strftime("%Y-%m-%d %H:%M")

        system_with_date = (
            SYSTEM_PROMPT
            + f"\n\nFecha actual: {ahora_str}. "
            "Cuando el usuario use palabras como 'hoy', 'mañana' o "
            "'pasado mañana', debes convertirlas SIEMPRE a fechas "
            "completas en formato 'YYYY-MM-DD HH:MM' usando esta "
            "fecha como referencia. "
            "Nunca pongas años anteriores al año actual salvo que "
            "el usuario lo pida explícitamente."
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_with_date}
        ]

        messages.extend(self.conversation_history)

        if user_message:
            messages.append({"role": "user", "content": user_message})

        return messages

    def _execute_tool(self, tool_name: str, tool_args: Dict) -> str:
        """
        Ejecuta una herramienta y retorna el resultado como string JSON.
        Intenta desenvolver wrappers tipo FunctionTool antes de llamar.
        """
        if tool_name not in self.tools_map:
            error_msg = f"Herramienta '{tool_name}' no encontrada"
            print("❌", error_msg)
            return json.dumps({"error": error_msg}, ensure_ascii=False)

        # Recuperamos el objeto registrado
        function = self.tools_map[tool_name]

        # Desenvuelto de wrappers (por ejemplo, FunctionTool)
        # Intentamos quedarnos con una función realmente invocable
        if not callable(function):
            # Caso típico: objetos con atributo .func o .fn que es la función real
            if hasattr(function, "func") and callable(function.func):
                function = function.func
            elif hasattr(function, "fn") and callable(function.fn):
                function = function.fn
            elif hasattr(function, "__call__"):
                function = function.__call__

        try:
            result = function(**tool_args)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            error_msg = f"Error ejecutando {tool_name}: {str(e)}"
            print("❌", error_msg)
            return json.dumps({"error": error_msg}, ensure_ascii=False)

    def chat(self, user_message: str, max_turns: int = 10) -> str:
        """
        Procesa un mensaje del usuario con soporte para tool calling.
        Hace varias iteraciones como máximo (max_turns) por si el modelo
        encadena varias llamadas a herramientas.
        """
        # Añadimos el mensaje del usuario al historial
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        turn = 0

        while turn < max_turns:
            messages = self._build_messages()

            try:
                response = self.client.chat_completion(
                    messages=messages,
                    tools=self.tools_schema if self.tools_schema else None,
                    tool_choice="auto",
                    max_tokens=1000,
                    temperature=0.7
                )

                assistant_message = response.choices[0].message

                # Caso 1: el modelo quiere usar herramientas
                if hasattr(assistant_message, "tool_calls") and assistant_message.tool_calls:
                    # Si el modelo ha generado algo de texto antes de las tool calls, lo guardamos
                    if assistant_message.content:
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": assistant_message.content
                        })

                    # Ejecutamos cada herramienta solicitada
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        raw_args = tool_call.function.arguments

                        # Parseo robusto de argumentos
                        if not raw_args:
                            tool_args = {}
                        else:
                            try:
                                if isinstance(raw_args, dict):
                                    tool_args = raw_args
                                else:
                                    tool_args = json.loads(raw_args)
                            except Exception as e:
                                print(f"Error parseando argumentos de {tool_name}: {raw_args} -> {e}")
                                tool_args = {}

                        print(f"🔧 Ejecutando: {tool_name}({tool_args})")

                        tool_result = self._execute_tool(tool_name, tool_args)

                        # En lugar de role "tool", añadimos el resultado como un mensaje de usuario
                        # para que Hugging Face no dé error y el modelo pueda usar la info.
                        self.conversation_history.append({
                            "role": "user",
                            "content": (
                                f"Resultado de la herramienta '{tool_name}' "
                                f"con argumentos {tool_args}:\n{tool_result}"
                            )
                        })

                    turn += 1
                    # Volvemos al principio del bucle: ahora el modelo verá en el historial
                    # el resultado de las tools e intentará dar una respuesta final.
                    continue

                # Caso 2: el modelo da una respuesta final normal
                else:
                    final_response = assistant_message.content

                    self.conversation_history.append({
                        "role": "assistant",
                        "content": final_response
                    })

                    return final_response

            except Exception as e:
                # Cualquier error en la llamada a la API se captura aquí
                error_text = f"Lo siento, hubo un error al procesar tu solicitud: {str(e)}"
                print("❌ Error en chat():", e)

                if turn == 0:
                    return error_text
                else:
                    return "He procesado tu solicitud pero encontré un error al generar la respuesta final."

        # Si se llega aquí, se alcanzó el máximo de iteraciones
        return "Se alcanzó el límite de iteraciones internas. Por favor, reformula tu pregunta."

    def reset_conversation(self):
        """Reinicia el historial de conversación."""
        self.conversation_history = []
