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

        # Interesado en
        "custentity_ap_sp_interesado_en_form_onli": {
            "id": 1
        },

        # Forma de contacto
        "custentity_ap_sp_forma_de_contactoi": {
            "id": 1
        },

        # Dirección
        "addressbook": {
            "items": [
                {
                    "defaultBilling": True,
                    "defaultShipping": True,
                    "addressbookaddress": {
                        "addr1": "Av. Siempre Viva 742",
                        "custrecord_l54_provincia": "1",
                        "city": "La Plata",
                        "zip": "1000",
                        "country": "AR"
                    }
                }
            ]
        }
    }
