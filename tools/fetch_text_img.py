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


# class ChangesInAFile(BaseModel):
#     additions: int = Field(..., description="Number of lines added")
#     changes: int = Field(..., description="Number of changes")
#     deletions: int = Field(..., description="Number of lines deleted")
#     filename: str = Field(..., description="Name of the changed file")
#     patch: str = Field(..., description="Patch text which shows the changes")
#     sha: str = Field(..., description="Commit SHA for the file")
#     status: str = Field(..., description="File status (added, removed, modified, etc.)")
    

    # imp
class FetchTextAndImgSchema(BaseModel):
    commits:str = Field(..., description="The commits which will be used to generate code summary and code snippet.")
 

class FetchTextAndImgTool(Tool[str]):
    id : str = "0002"
    name:str="Get push summary and code snippet"
    description: str = "This tool returns the short summary of the github push made and it also gives the code snippet of the code pushed"
    # imp
    args_schema: type[BaseModel] = FetchTextAndImgSchema
    # imp

    output_schema: tuple[str, str]=(
        "str",
        "code changes summary"
    )
    # imp
    def run(self, _: ToolRunContext, commits: str) -> str | None :

        load_dotenv()
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

        llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash" ,
        api_key=GOOGLE_API_KEY
        )

        messages = [
            SystemMessage(content=(
                "You are a code summariser. "
                "Check the provided GitHub commit data and generate a very short summary "
                "and a valid code snippet of the important changes."
                "Respond ONLY in this text format NOT json:\n"
                "  code summary: <short summary>,\n"
                "  code snippet: <code snippet>\n"
            )),
            HumanMessage(content=f"Generate the summary for these commits:\n{commits}")
        ]
        try:
            ai_msg = llm.invoke(messages)
            print(ai_msg.content)
            return f"{ai_msg.content}"
        except Exception as e:
            print("\nError occured in llm significance")
            print(e)
            return f"{e}"

