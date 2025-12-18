# mapper.py

def build_netsuite_lead(ghl: dict) -> dict:
    location = ghl.get("location", {}) or {}

    return {
        # Nombre del lead
        "companyName": ghl.get("full_name") or "Lead desde GHL",

        # Email (si existe)
        "email": ghl.get("email"),

        # Estado Lead
        "entityStatus": {
            "id": "37"  # 👈 Lead - ajustá si cambia
        },

        # Obligatorio OneWorld
        "subsidiary": {
            "id": "2"
        },

        # Origen del lead
        "leadsource": {
            "id": 135179
        },

        # Dirección
        "addressbook": {
            "items": [
                {
                    "defaultBilling": True,
                    "defaultShipping": True,
                    "addressbookaddress": {
                        "addr1": location.get("address"),
                        "city": location.get("city"),
                        "zip": location.get("postalCode"),
                        "country": "AR"
                    }
                }
            ]
        }
    }
