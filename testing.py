# import json
# from pydantic import BaseModel, Field, ValidationError
# import pprint
# class ChangesInAFile(BaseModel):
#     additions: int = Field(..., description="Number of lines added")
#     changes: int = Field(..., description="Number of changes")
#     deletions: int = Field(..., description="Number of lines deleted")
#     filename: str = Field(..., description="Name of the changed file")
#     patch: str = Field(..., description="Patch text which shows the changes")
#     sha: str = Field(..., description="Commit SHA for the file")
#     status: str = Field(..., description="File status (added, removed, modified, etc.)")

# class FindSignificanceToolSchema(BaseModel):

#     commits:list[list[ChangesInAFile]] = Field(..., description="The city to get the weather for")

# data={'commits': [[{'sha': '01448a8bccaa074900d0b8aca570139d517f6e4d', 'filename': 'hello.c', 'status': 'added', 'additions': 6, 'deletions': 0, 'changes': 6, 'patch': '@@ -0,0 +1,6 @@\n+#include<stdio.h>\n+int main()\n+{\n+  printf("Hello Wrold");\n+  return 0;\n+}'}]]}

# try:
#     commits = FindSignificanceToolSchema(**data)
#     print(commits)
# except ValidationError as e:
#     print("Error in validation")
#     print(e)

# data= {
#     'value': (
#         '{"content":"Low Significance","additional_kwargs":{},"response_metadata":{'
#         '"prompt_feedback":{"block_reason":0,"safety_ratings":[]},"finish_reason":"STOP",'
#         '"model_name":"gemini-2.0-flash","safety_ratings":[]},"type":"ai","name":null,'
#         '"id":"run--f78d2e27-b2e3-4c13-9d6c-0e4c1a598b4a-0","example":false,"tool_calls":[],'
#         '"invalid_tool_calls":[],"usage_metadata":{"input_tokens":183,"output_tokens":3,'
#         '"total_tokens":186,"input_token_details":{"cache_read":0}}}'
#     ),
#     'summary': (
#         'The code change, adding a "hello.c" file with a basic "Hello World" program, '
#         'is determined to have low significance.'
#     ),
# }
# print(data['summary'])
# print(type((data['summary'])))

# # import logging
# # logging.basicConfig(level=logging.DEBUG)

# # import os
# # from slack_sdk import WebClient
# # from slack_sdk.errors import SlackApiError
# # import dotenv

# # dotenv.load_dotenv()
# # slack_token = os.getenv("SLACK_BOT_TOKEN")
# # client = WebClient(token=slack_token)

# # try:
# #     # response = client.chat_postMessage(
# #     #     channel="C09C3LPNNC9",
# #     #     text="Hello from your app! :tada:"
# #     # )
# #     response = client.files_upload_v2(
# #     file="temp_img.png",
# #     text="Here",
# #     title="Test upload",
# #     channel="C09C3LPNNC9",
# #     initial_comment="Here is the latest version of the file!",
# #     )
# # except SlackApiError as e:
# #     # You will get a SlackApiError if "ok" is False
# #     assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'