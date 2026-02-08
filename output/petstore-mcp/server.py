from __future__ import annotations
import asyncio, json, os
from typing import Any
import httpx
from dedalus_mcp import MCPServer, tool

BASE_URL = os.getenv("PETSTORE_API_BASE_URL", "https://petstore.example.com/api/v1")
API_KEY = os.getenv("PETSTORE_API_API_KEY", "")

def _headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if API_KEY:
        h["X-API-Key"] = API_KEY
    return h

async def _request(method: str, path: str, *, params: dict[str, Any] | None = None,
                   body: dict[str, Any] | None = None) -> str:
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(method, url, headers=_headers(),
                                      params=params, json=body if body else None)
            resp.raise_for_status()
            try:
                return json.dumps(resp.json(), indent=2)
            except Exception:
                return resp.text
        except httpx.HTTPStatusError as e:
            return json.dumps({"error": str(e), "status": e.response.status_code})
        except Exception as e:
            return json.dumps({"error": str(e)})

@tool(description="Mark a pet as adopted [WRITES DATA]")
async def adoptpet(petId: int, owner_id: int, notes: str | None = None) -> str:
    """Mark a pet as adopted."""
    body: dict[str, Any] = {"owner_id": owner_id}
    if notes is not None:
        body["notes"] = notes
    return await _request("POST", f"/pets/{petId}/adopt", body=body)

@tool(description="Register a new owner [WRITES DATA]")
async def createowner(name: str, email: str, id: int | None = None, phone: str | None = None) -> str:
    """Register a new owner."""
    body: dict[str, Any] = {"name": name, "email": email}
    if id is not None:
        body["id"] = id
    if phone is not None:
        body["phone"] = phone
    return await _request("POST", "/owners", body=body)

@tool(description="Add a new pet [WRITES DATA]")
async def createpet(name: str, species: str, id: int | None = None, breed: str | None = None,
                   age: int | None = None, status: str | None = None) -> str:
    """Add a new pet."""
    body: dict[str, Any] = {"name": name, "species": species}
    if id is not None:
        body["id"] = id
    if breed is not None:
        body["breed"] = breed
    if age is not None:
        body["age"] = age
    if status is not None:
        body["status"] = status
    return await _request("POST", "/pets", body=body)

@tool(description="Delete an owner record [DESTRUCTIVE — may permanently delete data]")
async def deleteowner(ownerId: int) -> str:
    """Delete an owner record."""
    return await _request("DELETE", f"/owners/{ownerId}")

@tool(description="Delete a pet [DESTRUCTIVE — may permanently delete data]")
async def deletepet(petId: int) -> str:
    """Delete a pet."""
    return await _request("DELETE", f"/pets/{petId}")

@tool(description="Search or list owners with flexible filtering.")
async def search_owners(ownerId: int | None = None, limit: int | None = None,
                       offset: int | None = None) -> str:
    """Search or list owners."""
    if ownerId is not None:
        path = f"/owners/{ownerId}"
        return await _request("GET", path)
    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return await _request("GET", "/owners", params=params)

@tool(description="Search or list pets with flexible filtering.")
async def search_pets(petId: int | None = None, species: str | None = None,
                     status: str | None = None, limit: int | None = None,
                     offset: int | None = None, q: str | None = None) -> str:
    """Search or list pets."""
    if petId is not None:
        return await _request("GET", f"/pets/{petId}")
    params: dict[str, Any] = {}
    if species is not None:
        params["species"] = species
    if status is not None:
        params["status"] = status
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if q is not None:
        params["q"] = q
        return await _request("GET", "/pets/search", params=params)
    return await _request("GET", "/pets", params=params)

@tool(description="Update a pet [WRITES DATA]")
async def updatepet(petId: int, name: str, species: str, id: int | None = None,
                   breed: str | None = None, age: int | None = None,
                   status: str | None = None) -> str:
    """Update a pet."""
    body: dict[str, Any] = {"name": name, "species": species}
    if id is not None:
        body["id"] = id
    if breed is not None:
        body["breed"] = breed
    if age is not None:
        body["age"] = age
    if status is not None:
        body["status"] = status
    return await _request("PUT", f"/pets/{petId}", body=body)

server = MCPServer("petstore")
server.collect(
    adoptpet,
    createowner,
    createpet,
    deleteowner,
    deletepet,
    search_owners,
    search_pets,
    updatepet
)
if __name__ == "__main__":
    asyncio.run(server.serve())