from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import iscc_core as ic
from starlette.middleware.cors import CORSMiddleware
import iscc_flake


docs = """
## Generator for distributed unique time-ordered IDs

The [ISCC Flake-Code](https://core.iscc.codes/units/code_flake/) is unique, time-sorted
identifier composed of an 48-bit timestamp and 16 to 208 bit randomness.

It is a flexible implementation of a [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID)
that can be generated in various bit-sizes and converted into different representations.

### Get your Flake-ID

- Get 64-bit Flake-ID: [https://flake.iscc.io/flake](/flake)
- Get unique 128-bit Flake-ID: [https://flake.iscc.io//flake?bits=128](/flake?bits=128)
- Get globally unique 256-bit Flake-ID: https://flake.iscc.io/flake?bits=256

### Interactive API docs at [https://flake.iscc.io/try-it](/try-it)
"""


app = FastAPI(
    title="ISCC - Flake-ID Generator",
    version=iscc_flake.__version__,
    description=docs,
    docs_url="/try-it",
    redoc_url="/",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class FlakeID(BaseModel):
    iscc: str = Field(
        ...,
        description="Flake-ID in canonical **ISCC-CODE** URI-representation (self-describing)",
        example="ISCC:OAAQC773TKQVOR62",
        max_length=73,
        min_length=15,
        regex="^ISCC:[A-Z2-7]{10,73}$",
    )
    string: str = Field(
        ...,
        description="Flake-Code as base32hex string with lexicographic sorting",
        example="05VVN6L1AT3TK",
    )
    integer: str = Field(
        ...,
        description="Flake-Code as time-sortable integer (string-wrapped)",
        example="108081557630568410",
    )
    time: datetime = Field(
        ...,
        description="Time component of Flake-Code as string in ISO 8601 format",
        example="2022-04-05T21:21:29.431000",
    )


def flake(bits: int):
    try:
        f = ic.Flake(bits=bits)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    return FlakeID(iscc=f.iscc, string=f.string, integer=str(f.int), time=f.time)


@app.post("/", response_model=FlakeID, tags=["flake"], status_code=status.HTTP_201_CREATED)
async def create_flake(bits: Optional[int] = 64):
    """Create Flake-ID"""
    return flake(bits)


@app.get("/flake", response_model=FlakeID, tags=["flake"])
async def get_flake(bits: Optional[int] = 64):
    """Get Flake-ID"""
    return flake(bits)
