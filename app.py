import os
import subprocess
from typing import Dict, Any
from aioboto3 import Session
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from json import loads
from typing import Dict, Any
from models import LambdaFunction

session = Session()


def isdirectory(x):
    if x["Size"] == 0:
        return "directory"
    else:
        return "file"


app = FastAPI()


@app.post("/api/upload/{sub}")
async def lambda_endpoint(sub: str, name: str, body=Body(...)):
    if name.endswith(".py"):
        content_type = "text/x-python"
    elif name.endswith(".js"):
        content_type = "application/javascript"
    elif name.endswith(".html"):
        content_type = "text/html"
    elif name.endswith(".css"):
        content_type = "text/css"
    elif name.endswith(".json"):
        content_type = "application/json"
    else:
        content_type = "text/plain"
    async with session.client("s3") as s3:
        await s3.put_object(
            Bucket="cdn.hatarini.com",
            Key=f"{sub}/lambda/{name}",
            Body=loads(body)["code"],
            ACL="public-read",
            ContentType=content_type,
        )


@app.get("/api/upload/{sub}")
async def workspace_endpoint(sub: str):
    async with session.client("s3") as s3:
        response = await s3.list_objects_v2(
            Bucket="cdn.hatarini.com", Prefix=f"{sub}/lambda/"
        )
        response.pop("ResponseMetadata")
        return [
            {
                "name": f"{i['Key'].split('lambda/')[1]}",
                "url": f"https://s3.amazonaws.com/cdn.hatarini.com/{i['Key']}",
                "type": isdirectory(i),
            }
            for i in response["Contents"]
        ]


@app.get("/api/upload/")
async def upload_endpoint(key: str):
    async with session.client("s3") as s3:
        await s3.list_objects_v2(Bucket="cdn.hatarini.com", Prefix=f"{key}/")


@app.delete("/api/upload/")
async def delete_endpoint(key: str):
    async with session.client("s3") as s3:
        await s3.delete_object(Bucket="cdn.hatarini.com", Key=key)


@app.get("/api/download/")
async def download_endpoint(key: str):
    async with session.client("s3") as s3:
        response = await s3.get_object(Bucket="cdn.hatarini.com", Key=key)
        return (await response["Body"].read()).decode("utf-8")


@app.get("/api/download/zip/{sub}")
async def zip_endpoint(sub: str):
    async with session.client("s3") as s3:
        subprocess.run(["rm", "-rf", "static/*"])
        response = await s3.list_objects_v2(
            Bucket="cdn.hatarini.com", Prefix=f"{sub}/lambda/"
        )
        response.pop("ResponseMetadata")
        response = [
            {
                "key": i["Key"],
                "url": f"https://s3.amazonaws.com/cdn.hatarini.com/{i['Key']}",
                "type": isdirectory(i),
            }
            for i in response["Contents"]
        ]
        try:
            for i in response:
                with open(f"static/{i['key'].split('lambda/')[1]}", "w") as f:
                    f.write(await download_endpoint(i["key"]))
        except:
            pass
        os.chdir("static")
        try:
            subprocess.run(
                [
                    "pip",
                    "install",
                    "-r",
                    "requirements.txt",
                    "-t",
                    ".",
                    "--upgrade",
                    "--no-cache-dir",
                ]
            )
        except:
            pass
        subprocess.run(["zip", "-r", "app.zip", "."])
        os.chdir("..")
        return FileResponse(
            "static/app.zip", media_type="application/zip", filename="app.zip"
        )


@app.post("/api/deploy/{sub}")
async def create_function(sub: str) -> Dict[str, Any]:
    async with session.client("lambda") as lambda_:
        returnable = await lambda_.create_function(
            FunctionName=uuid4().hex,
            Runtime="python3.8",
            Role="arn:aws:iam::992472819525:role/service-role/search-role-x0hu2si7",
            Handler=f"app.handler",
            Code={"ZipFile": open("static/app.zip", "rb").read(),},
            Timeout=3,
            MemorySize=128,
            Publish=True,
        )
        url = await lambda_.create_function_url_config(
            FunctionName=returnable["FunctionName"],
            AuthType="NONE",
            Cors={
                "AllowOrigins": ["*"],
                "AllowMethods": ["*"],
                "AllowHeaders": ["*"],
                "AllowCredentials": True,
                "ExposeHeaders": ["*"],
                "MaxAge": 86400,
            },
        )
        await lambda_.add_permission(
            FunctionName=returnable["FunctionName"],
            StatementId=uuid4().hex,
            Action="lambda:InvokeFunctionUrl",
            Principal="*",
            FunctionUrlAuthType="NONE",
        )
        returnable = {
            "url": url["FunctionUrl"],
            "name": returnable["FunctionName"],
            "arn": returnable["FunctionArn"],
        }
        func = LambdaFunction(
            sub=sub,
            name=returnable["name"],
            arn=returnable["arn"],
            url=returnable["url"],
        )
        print(func.json())
        func.save()
        return returnable

@app.get("/api/deploy/{sub}")
async def list_functions(sub: str) -> Dict[str, Any]:
    res = LambdaFunction.find_many(field="sub", value=sub)
    print(res)
    return res

www = StaticFiles(directory="www", html=True)
static = StaticFiles(directory="static", html=True)

 
@app.delete("/api/deploy/{sub}")
async def delete_function(sub:str, name:str):
    async with session.client("lambda") as lambda_:
        LambdaFunction.delete(field="name", value=name)
        await lambda_.delete_function(FunctionName=name)
    return {"status": "ok"}   

app.mount("/static", static, name="static")


@app.get("/favicon.ico")
@app.get("/favicon.svg")
@app.get("/favicon.png")
@app.get("/vite.svg")
def favicon():
    return FileResponse("www/vite.svg")

@app.get("/favicon.gif")
def favicon_gif():
    return FileResponse("www/favicon.gif")

assets = StaticFiles(directory="www/assets", html=True)
app.mount("/assets", assets, name="assets")


@app.get("/")
def index():
    return FileResponse("www/index.html")
