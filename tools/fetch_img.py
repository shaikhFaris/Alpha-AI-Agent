import os
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
    code_snippet:str = Field(..., description="The condensed code snippet of the github push changes.")
 

class FetchImgTool(Tool[str]):
    id : str = "0003"
    name:str="Fetch Code SNippet Image"
    description: str = "Gets code snippet image from a backend."
    # imp
    args_schema: type[BaseModel] = FetchImgSchema
    # imp
    output_schema: tuple[str, str]=(
        "str",
        "image data"
    )
    # imp
    def run(self, _: ToolRunContext, code_snippet: str) -> str | None :
        print(code_snippet)
        return None


