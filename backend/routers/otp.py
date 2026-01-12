from fastapi import APIRouter, HTTPException, Form
from random import randint
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Mobile OTP"]
)

otp_store = {}  # For demo only; use Redis in production

@router.post("/send-otp")
def send_otp(mobile: str = Form(...)):
    otp = randint(1000, 9999)
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    otp_store[mobile] = {"otp": otp, "expires_at": expires_at}

    # TODO: Send SMS via Twilio or any gateway
    print(f"OTP for {mobile}: {otp}")  # For testing

    return {"msg": f"OTP sent to {mobile}"}

@router.post("/verify-otp")
def verify_otp(mobile: str = Form(...), otp: int = Form(...)):
    if mobile not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not sent for this number")

    otp_data = otp_store[mobile]
    if datetime.utcnow() > otp_data["expires_at"]:
        del otp_store[mobile]
        raise HTTPException(status_code=400, detail="OTP expired")

    if otp_data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Incorrect OTP")

    del otp_store[mobile]
    return {"msg": "Mobile verified successfully"}
