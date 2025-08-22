import os
import json
import pprint
from dotenv import load_dotenv
from portia import (
    Config,
    LLMProvider,
    Portia,
    example_tool_registry,
)
from tools.find_significance import FindSignificanceTool
from tools.fetch_text_img import FetchTextAndImgTool
from tools.fetch_img import FetchImgTool


def init_agent(code):
    print("loading env...")

    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    # Create a default Portia config with LLM provider set to Google GenAI and model set to Gemini 2.0 Flash
    google_config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        default_model="google/gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        default_log_level="INFO"
    )
    # Instantiate a Portia instance. Load it with the config and with the example tools.
    portia = Portia(config=google_config, tools=[FindSignificanceTool(),FetchTextAndImgTool(),FetchImgTool()])

    print("portia planning and running...")

    # if you get error here, then it is most probably in tools
    plan = portia.plan(f"""
You will a github push made by a user to a particular repo. It will be provides here below:
{code}
First get significance of the code changes made in this github push. Then get the code summary and code snippet. Extract the code snippet in text format from the code_snippet get an image from it.
    """)
    print(plan)
    print(plan.pretty_print())

    # running the damn plan
    portia.run_plan(plan)


    # # # gives dict 
    # dict_output=json.loads(plan.model_dump_json(indent=2))

    # pprint.pprint(dict_output)

    # # data that we want
    # imp_data:dict= json.loads(dict_output["outputs"]["final_output"]["value"])
    # summary:str=dict_output["outputs"]["final_output"]["summary"]

    # print("\n\n")
    # pprint.pprint(imp_data)
    # print(f"\033[92m{summary}\033[0m")


# code={'commits': [[{'sha': '01448a8bccaa074900d0b8aca570139d517f6e4d', 'filename': 'hello.c', 'status': 'added', 'additions': 6, 'deletions': 0, 'changes': 6, 'patch': '@@ -0,0 +1,6 @@\n+#include<stdio.h>\n+int main()\n+{\n+  printf("Hello Wrold");\n+  return 0;\n+}'}]]}

# init_agent({'commits': [[{'additions': 1,
#                'changes': 2,
#                'deletions': 1,
#                'filename': 'complex.c',
#                'patch': '@@ -1,7 +1,7 @@\n'
#                         ' #include <stdio.h>\n'
#                         ' \n'
#                         ' int mystery(int *arr, int n) {\n'
#                         '-    if (n/0 == 0) return 0;\n'
#                         '+    if (n/0 == 0) return 0/12;\n'
#                         '     return (arr[n - 1] ^ n) + mystery(arr, n - 1);\n'
#                         ' }\n'
#                         ' ',
#                'sha': 'b139413b8ae973bc5ccec61afaae1c43427355d6',
#                'status': 'modified'}]]})