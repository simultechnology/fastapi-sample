from time import sleep
import asyncio

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


@app.get("/")
async def root():
    print('receive request!')
    return {"message": "Hello World"}


async def write_async_notification(filename: str, email: str, message=""):
    with open(filename, mode="a") as email_file:
        for i in range(10):
            content = f"{i}: notification for {email}: {message}"
            print(content)
            email_file.write(f"{content}\n")
            await asyncio.sleep(1)


@app.get("/send_async_notification")
async def send_async_notification(background_tasks: BackgroundTasks):
    email = "test@test.com"
    background_tasks.add_task(write_async_notification, "log_async_0.txt", email, message="some notification")
    await asyncio.gather(
        write_async_notification("log_async_1.txt",  email, message="await async notification"),
        write_async_notification("log_async_2.txt", email, message="await2 async notification")
    )
    # await write_notification("log_1.txt", "test@test.com", message="await notification")
    # await write_notification("log_2.txt", "test2@test.com", message="await2 notification")
    return {"message": "Notification sent in the background"}


def write_notification(filename: str, email: str, message=""):
    with open(filename, mode="a") as email_file:
        for i in range(10):
            content = f"{i}: notification for {email}: {message}"
            print(content)
            email_file.write(f"{content}\n")
            sleep(1)


@app.get("/send_notification")
def send_notification(background_tasks: BackgroundTasks):
    email = "test2@test.com"
    background_tasks.add_task(write_notification, "log_0.txt", email, message="some notification")
    write_notification("log_1.txt", email, message="await notification"),
    write_notification("log_2.txt", email, message="await2 notification")
    # await write_notification("log_1.txt", "test@test.com", message="await notification")
    # await write_notification("log_2.txt", "test2@test.com", message="await2 notification")
    return {"message": "Notification sent in the background"}
