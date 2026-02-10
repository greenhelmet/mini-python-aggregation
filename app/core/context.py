from contextvars import ContextVar, Token

REQUEST_ID_CTX_KEY = "request_id"

request_id_ctx_var: ContextVar[str] = ContextVar(
    REQUEST_ID_CTX_KEY,
    default="",
)

def set_request_id(request_id: str) -> Token:
    return request_id_ctx_var.set(request_id)

def reset_request_id(token: Token) -> None:
    request_id_ctx_var.reset(token)

def get_request_id() -> str:
    return request_id_ctx_var.get()