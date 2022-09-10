from fastapi import FastAPI

app = FastAPI(title="EvenLess")


@app.get("/")
def get_root() -> str:
    return "Hello World"
