#!/bin/bash

# Exit script if any command fails
/usr/bin/env /usr/local/bin/python -m uvicorn main:app --reload --port 8000 \
                                    --host 0.0.0.0 --log-level debug \
                                    --reload-dir /workspaces/portal-chat-api/app