from fastapi import FastAPI, Request
from oauth import get_netsuite_token
from netsuite import create_lead
from mapper import build_netsuite_lead

app = FastAPI()

@app.post("/ghl/contact-created")
async def receive_contact(request: Request):
    ghl_payload = await request.json()

    print("📩 Contacto GHL recibido")

    lead_payload = build_netsuite_lead(ghl_payload)

    token = get_netsuite_token()
    status, body = create_lead(token, lead_payload)

    print(f"📤 NetSuite response: {status}")

    return {
        "netsuite_status": status
    }

