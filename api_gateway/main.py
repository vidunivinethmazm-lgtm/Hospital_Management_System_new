from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
import httpx

SECRET_KEY = "hospital_mgmt_secret_key_2026"
ALGORITHM = "HS256"

PUBLIC_PATHS = {"/", "/health", "/docs", "/redoc", "/openapi.json",
                "/auth/register", "/auth/login", "/auth/users"}

app = FastAPI(
    title="Hospital Management - API Gateway",
    description="""
## API Gateway for Hospital Management System

Single entry point for all microservices. All protected routes require a JWT token.

**Step 1** — Register: `POST /auth/register`
**Step 2** — Login: `POST /auth/login` → copy the `access_token`
**Step 3** — Use token in Postman: Authorization tab → Bearer Token → paste token

| Service             | Port | Gateway Prefix   |
|---------------------|------|------------------|
| Auth Service        | 8007 | /auth            |
| Patient Service     | 8001 | /patients        |
| Doctor Service      | 8002 | /doctors         |
| Appointment Service | 8003 | /appointments    |
| Department Service  | 8004 | /departments     |
| Medicine Service    | 8005 | /medicines       |
| Bill Service        | 8006 | /bills           |
""",
    version="1.0.0",
)

SERVICES = {
    "auth":         "http://localhost:8007",
    "patients":     "http://localhost:8001",
    "doctors":      "http://localhost:8002",
    "appointments": "http://localhost:8003",
    "departments":  "http://localhost:8004",
    "medicines":    "http://localhost:8005",
    "bills":        "http://localhost:8006",
}


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS or request.url.path.startswith("/auth"):
            return await call_next(request)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Token missing. Login at POST /auth/login first."},
                status_code=401,
            )
        token = auth_header.split(" ")[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return JSONResponse(
                {"detail": "Invalid or expired token. Login again at POST /auth/login."},
                status_code=401,
            )
        return await call_next(request)


app.add_middleware(JWTMiddleware)


async def proxy(request: Request, service_url: str, path: str):
    url = f"{service_url}/{path}"
    query = request.url.query
    if query:
        url = f"{url}?{query}"
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.request(
                method=request.method, url=url, content=body, headers=headers,
            )
            return JSONResponse(
                content=response.json() if response.content else {},
                status_code=response.status_code,
            )
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"Service at {service_url} is unavailable.")


@app.get("/", tags=["Gateway"])
def gateway_root():
    return {"service": "Hospital Management API Gateway", "status": "running"}


@app.get("/health", tags=["Gateway"])
async def health_check():
    status = {}
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in SERVICES.items():
            try:
                r = await client.get(f"{url}/")
                status[name] = "up" if r.status_code == 200 else "degraded"
            except Exception:
                status[name] = "down"
    return {"gateway": "up", "services": status}


# ---------- Auth routes (public - no token needed) ----------
@app.api_route("/auth/register", methods=["POST"], tags=["Auth"])
async def auth_register(request: Request):
    return await proxy(request, SERVICES["auth"], "auth/register")


@app.api_route("/auth/login", methods=["POST"], tags=["Auth"])
async def auth_login(request: Request):
    return await proxy(request, SERVICES["auth"], "auth/login")


@app.api_route("/auth/users", methods=["GET"], tags=["Auth"])
async def auth_users(request: Request):
    return await proxy(request, SERVICES["auth"], "auth/users")


# ---------- Patient routes (token required) ----------
@app.api_route("/patients", methods=["GET", "POST"], tags=["Patients"])
async def patients_root(request: Request):
    return await proxy(request, SERVICES["patients"], "patients")


@app.api_route("/patients/{patient_id}", methods=["GET", "PUT", "DELETE"], tags=["Patients"])
async def patients_item(request: Request, patient_id: int):
    return await proxy(request, SERVICES["patients"], f"patients/{patient_id}")


# ---------- Doctor routes (token required) ----------
@app.api_route("/doctors", methods=["GET", "POST"], tags=["Doctors"])
async def doctors_root(request: Request):
    return await proxy(request, SERVICES["doctors"], "doctors")


@app.api_route("/doctors/{doctor_id}", methods=["GET", "PUT", "DELETE"], tags=["Doctors"])
async def doctors_item(request: Request, doctor_id: int):
    return await proxy(request, SERVICES["doctors"], f"doctors/{doctor_id}")


# ---------- Appointment routes (token required) ----------
@app.api_route("/appointments", methods=["GET", "POST"], tags=["Appointments"])
async def appointments_root(request: Request):
    return await proxy(request, SERVICES["appointments"], "appointments")


@app.api_route("/appointments/{appointment_id}", methods=["GET", "PUT", "DELETE"], tags=["Appointments"])
async def appointments_item(request: Request, appointment_id: int):
    return await proxy(request, SERVICES["appointments"], f"appointments/{appointment_id}")


# ---------- Department routes (token required) ----------
@app.api_route("/departments", methods=["GET", "POST"], tags=["Departments"])
async def departments_root(request: Request):
    return await proxy(request, SERVICES["departments"], "departments")


@app.api_route("/departments/{department_id}", methods=["GET", "PUT", "DELETE"], tags=["Departments"])
async def departments_item(request: Request, department_id: int):
    return await proxy(request, SERVICES["departments"], f"departments/{department_id}")


# ---------- Medicine routes (token required) ----------
@app.api_route("/medicines", methods=["GET", "POST"], tags=["Medicines"])
async def medicines_root(request: Request):
    return await proxy(request, SERVICES["medicines"], "medicines")


@app.api_route("/medicines/{medicine_id}", methods=["GET", "PUT", "DELETE"], tags=["Medicines"])
async def medicines_item(request: Request, medicine_id: int):
    return await proxy(request, SERVICES["medicines"], f"medicines/{medicine_id}")


# ---------- Bill routes (token required) ----------
@app.api_route("/bills", methods=["GET", "POST"], tags=["Bills"])
async def bills_root(request: Request):
    return await proxy(request, SERVICES["bills"], "bills")


@app.api_route("/bills/{bill_id}", methods=["GET", "PUT", "DELETE"], tags=["Bills"])
async def bills_item(request: Request, bill_id: int):
    return await proxy(request, SERVICES["bills"], f"bills/{bill_id}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
