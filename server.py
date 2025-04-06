import uvicorn
import warnings

warnings.filterwarnings("ignore")
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="localhost", port=8000)
  
