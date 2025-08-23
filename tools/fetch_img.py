import os
import requests
import re, json
import pprint
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from portia.errors import ToolHardError, ToolSoftError
from portia.tool import Tool, ToolRunContext

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage


    # imp
class FetchImgSchema(BaseModel):
    code_snippet:str = Field(..., description="The extracted code snippet.")
 

class FetchImgTool(Tool[str]):
    id : str = "0003"
    name:str="Fetch Code SNippet Image"
    description: str = "Gets code snippet image from a backend and stores in the root directory."
    # imp
    args_schema: type[BaseModel] = FetchImgSchema
    # imp
    output_schema: tuple[str, str]=(
        "str",
        "image data"
    )
    # imp
    def run(self, _: ToolRunContext, code_snippet: str) -> str | None:
        print(code_snippet)

        try:
            response = requests.post(
                "http://localhost:4100/image", 
                json={"code": code_snippet},
            )

            # Check if response is image bytes
            if "image" in response.headers.get("Content-Type", ""):
                with open("temp_img.png", "wb") as f:
                    f.write(response.content)
                print("Image saved successfully.")
                return "Successfully stored code snippet image in root dir"
            else:
                print("Non-image response:", response.text)
                return "Fetched response but it wasn't an image."

        except Exception as e:
            return f"Request failed: {e}"



