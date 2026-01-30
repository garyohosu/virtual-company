# API Verification

## Startup
Attempting to start uvicorn server in-process.
Server started: True

## /api/health
Status: 404
Body: {"detail":"Not Found"}

## /api/check-limit
Status: 200
Body: {"allowed":true,"count":0,"limit":5,"isPremium":false}

Server stopped: True