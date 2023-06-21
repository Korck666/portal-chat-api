# app/services/ngrok.py
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

import requests
import uvicorn
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from app.services.healthcheck import HealthCheck

from app.utils.config import Config
from app.services.logger import Logger


class NgrokService(HealthCheck):
    def __init__(self, app, external_url):
        self.app = app
        self.config = Config()
        self.logger = Logger()
        self._process = None

    def start(self):
        if self.config.PUBLIC_URL == "localhost":
            # Start ngrok subprocess
            self._process = subprocess.Popen(["ngrok", "http", f"{self.config.EXPOSED_PORT}"])
            # Wait for ngrok to start up
            # ngrok_url = "http://localhost:4040/api/tunnels"
            max_retries = 5
            retry_count = 0
            while retry_count < max_retries:
                try:
                    response = requests.get(self.config.NGROK_TUNNEL_URL, timeout=1)
                    if response.status_code == 200:
                        break
                except (requests.exceptions.RequestException, requests.exceptions.Timeout):
                    pass
                retry_count += 1
                time.sleep(2)

            # Get ngrok public URL
            response = requests.get(self.config.NGROK_TUNNEL_URL).json()
            # Update external URL to ngrok public URL
            self.config.PUBLIC_URL = response["tunnels"][0]["public_url"]
            self.logger.info(f"Ngrok started at {self.config.PUBLIC_URL}")

        # Run FastAPI app
        #TODO: refactor the restart here and stop the ngrok subprocess
        uvicorn.run(self.app, host="0.0.0.0", port=8000, log_level=self.config.LOG_LEVEL)

    def stop(self):
        # Stop ngrok subprocess if running
        try:
            subprocess.run(["pkill", "ngrok"])
            self.logger.info("Ngrok stopped.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error stopping ngrok: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error stopping ngrok")
