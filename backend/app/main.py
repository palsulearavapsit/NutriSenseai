from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.analyze import router as analyze_router
from dotenv import load_dotenv
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.core.limiter import limiter

load_dotenv()

app = FastAPI()
app.include_router(analyze_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda r, e: JSONResponse(status_code=429, content={"error": "Too many requests"})
)

app.include_router(analyze_router)
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}