import uvicorn
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="localhost", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem",reload=True)
  