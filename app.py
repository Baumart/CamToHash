from fastapi import FastAPI, HTTPException
import uvicorn

from camCapture import (
    capture_entropy_blob_sha3_512,
    capture_entropy_blob_shake_256_1024
)

app = FastAPI(debug=False)


@app.get("/sha3-512")
async def generate_random_512():
    random_hash, error = capture_entropy_blob_sha3_512()
    if error:
        raise HTTPException(status_code=500, detail=error)
    return {"random_hash": random_hash}


@app.get("/")
async def generate_random_1024():
    random_hash, error = capture_entropy_blob_shake_256_1024()
    if error:
        raise HTTPException(status_code=500, detail=error)
    return {"random_hash": random_hash}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=443,
        ssl_certfile="cert/cert.pem",
        ssl_keyfile="cert/key.pem"
    )
