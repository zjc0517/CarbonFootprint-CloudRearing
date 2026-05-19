"""启动碳足迹API服务."""
import uvicorn
from carbon_engine.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
