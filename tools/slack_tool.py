import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import re, json
import pprint
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from portia.errors import ToolHardError, ToolSoftError
from portia.tool import Tool, ToolRunContext


    # imp
class SlackToolSchema(BaseModel):
    code_summary:str = Field(..., description="github changes summary text in short")
 

class SlackTool(Tool[str]):
    id : str = "0004"
    name:str="Slack Poster"
    description: str = "send code changes text summary to slack channel."
    # imp
    args_schema: type[BaseModel] = SlackToolSchema
    # imp
    output_schema: tuple[str, str]=(
        "str",
        "Output string indicating of the image and code summary was sent or not."
    )
    # imp
    def run(self, _: ToolRunContext, code_summary: str) -> str | None:
        load_dotenv()
        slack_token = os.getenv("SLACK_BOT_TOKEN")
        channel_id = "C09C3LPNNC9"
        image_path = "temp_img.png"

        load_dotenv()
        slack_token = os.getenv("SLACK_BOT_TOKEN")
        client = WebClient(token=slack_token)

        try:
            response = client.files_upload_v2(
            file=image_path,
            title="Code Snippet Summary",
            channel=channel_id,
            initial_comment=code_summary,
            )
            os.remove(image_path)
        except Exception as e:
            return f"An error occured in slack tool {e}"

