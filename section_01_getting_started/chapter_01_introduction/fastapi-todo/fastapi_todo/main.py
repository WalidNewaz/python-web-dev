from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint returning a welcome message.

    :return:
        dict[str, str]: JSON response with a message.
    """
    return {"message": "Welcome to FastAPI!"}