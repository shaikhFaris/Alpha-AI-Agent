import os
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
    

class FindSignificanceToolSchema(BaseModel):
    commits:str = Field(..., description="The commits which will be used to check if the code pushed is significant or not.")
 

class FindSignificanceTool(Tool[str]):
    id : str = "0001"
    name:str="Find Signficance Tool"
    description: str = "Finds whether the code pushed to the github repo is signicant or not."
    args_schema: type[BaseModel] = FindSignificanceToolSchema
    output_schema: tuple[str, str] = (
        "str",
        "String output indicating if the pushed code is significant or not significant"
    )

    
    def run(self, _: ToolRunContext, commits: str) -> str | None :

        load_dotenv()
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

        llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash" ,
        api_key=GOOGLE_API_KEY
        )

        messages = [
            SystemMessage(content="You are a code significance analyser which will rate the ONLY BASED ON THE CODE CHANGES IN THE PUSH NOT THE PREEXISTING CODE. ONLY CHANGES MADE IN PUSH"
            " There are 3 levels of significance - High Significance refers to  highly impactful code  which could potentially disrupt the code if the code has  system errors and if it crashes at  Runtime  and performance critical , medium Significance refers to the code which affects the functionality but not like high significance and low Significance means which does affect the functionality of the code or just the basic code like -comment,formatting changes ,repetitive code and minor ui change  ."),
            HumanMessage(content=f'Is this change significant\n{commits}. Give very short and to the point answer.')
        ]
        try:
            ai_msg = llm.invoke(messages)
            return f"significance tool returns: {ai_msg.content}"
        except Exception as e:
            print("\nError occured in llm significance")
            print(e)
            return f"Error eccoured in llm significance ferching {e}"

