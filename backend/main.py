from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.detect import router as detect_router
from backend.routes.review import router as review_router
from backend.routes import reviews


app = FastAPI(
    title="YAAR AI Design Mentor",
    description="Multimodal AI-powered UI design review assistant",
    version="1.0.0"
)


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# REGISTER ROUTES
# =========================================

app.include_router(detect_router)
app.include_router(review_router)
app.include_router(reviews.router)


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():
    return {
        "message": "YAAR AI Design Mentor API is running"
    }