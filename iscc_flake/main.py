from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import iscc_core as ic


app = FastAPI(
    title="FLake-ID generator",
    description="Generator for distributed unique time-ordered IDs",
    docs_url="/",
)


class FlakeID(BaseModel):
    iscc: str
    string: str
    int: str
    time: datetime


def flake(bits: int):
    try:
        f = ic.Flake(bits=bits)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    return FlakeID(iscc=f.iscc, string=f.string, int=str(f.int), time=f.time)


@app.post("/", response_model=FlakeID, tags=["flake"])
async def create_flake(bits: Optional[int] = 64):
    """Create Flake-ID"""
    return flake(bits)


@app.get("/flake", response_model=FlakeID, tags=["flake"])
async def get_flake(bits: Optional[int] = 64):
    """Get Flake-ID"""
    return flake(bits)
