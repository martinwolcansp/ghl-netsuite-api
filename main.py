from oauth import get_netsuite_token
from netsuite import create_lead

@app.post("/ghl/contact-created")
async def receive_contact(request: Request):
    payload = await request.json()

    token = get_netsuite_token()  # ✅ sin parámetros
    status, body = create_lead(token, payload)

    return {"netsuite_status": status}

