from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.agent.travel_agent import TravelPlanningAgent, TravelRequest


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Travel Planning Agent", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

agent = TravelPlanningAgent()


class PlanPayload(BaseModel):
    destination: str = Field(..., min_length=1)
    date: str = Field(..., min_length=1)
    preference: str = Field(default="")
    days: int = Field(..., gt=0)
    budget: int = Field(..., ge=0)
    travel_style: str = Field(default="standard")


def _build_response(payload: PlanPayload) -> Dict[str, Any]:
    result = agent.plan_trip(
        TravelRequest(
            destination=payload.destination.strip(),
            date=payload.date.strip(),
            preference=payload.preference.strip(),
            days=payload.days,
            budget=payload.budget,
            travel_style=payload.travel_style.strip(),
        )
    )
    return result


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "defaults": {
                "destination": "\u0110\u00e0 N\u1eb5ng",
                "date": "2026-06-15",
                "preference": "bi\u1ec3n v\u00e0 \u0103n u\u1ed1ng",
                "days": 3,
                "budget": 4000000,
                "travel_style": "standard",
            }
        },
    )


@app.post("/plan")
async def create_plan(payload: PlanPayload) -> Dict[str, Any]:
    try:
        return _build_response(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
