#!/usr/bin/env python3
import uvicorn

from noteit_api.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "noteit_api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        reload_dirs=["src/"]
    )