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
from tools.slack_tool import SlackTool


def init_agent(code):
    print("loading env...")

    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    # Create a default Portia config with LLM provider set to Google GenAI and model set to Gemini 2.0 Flash
    google_config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        default_model="google/gemini-2.5-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        default_log_level="INFO"
    )
    # Instantiate a Portia instance. Load it with the config and with the example tools.
    portia = Portia(config=google_config, tools=[FindSignificanceTool(),FetchTextAndImgTool(),FetchImgTool(),SlackTool()])

    print("portia planning and running...")

    # if you get error here, then it is most probably in tools
    plan = portia.plan(f"""
You will a github push made by a user to a particular repo. All the tools that you are provided with ONLY ACCEPT STRING AS ARGUMENT. It will be provides here below:
{code}
First get significance of the code changes made in this github push. Then get the code summary and code snippet. Then if the significance is low, ignore but if sginificance is medium or high Extract the code snippet in text format from code_snippet and get an image from it. Then send this text code summary in the slack channel.
    """)
    print(plan)
    print(plan.pretty_print())

    # running the damn plan
    run= portia.run_plan(plan)


    # # # gives dict 
    dict_output=json.loads(run.model_dump_json(indent=2))

    # pprint.pprint(dict_output)

    # # data that we want
    # imp_data:dict= json.loads(dict_output["outputs"]["final_output"]["value"])
    summary:str=dict_output["outputs"]["final_output"]["summary"]

    print("\n\n")
    print(f"\033[92m{summary}\033[0m")

# init_agent({'commits': [[{'additions': 37,
#                'changes': 37,
#                'deletions': 0,
#                'filename': 'routes.ts',
#                'patch': '@@ -0,0 +1,37 @@\n'
#                         '+import { Router, Request, Response } from '
#                         "'express';\n"
#                         "+import { PrismaClient } from '@prisma/client';\n"
#                         '+\n'
#                         '+const router = Router();\n'
#                         '+const prisma = new PrismaClient();\n'
#                         '+\n'
#                         '+// POST /users - create a new user\n'
#                         "+router.post('/users', async (req: Request, res: "
#                         'Response) => {\n'
#                         '+  const { name, email } = req.body;\n'
#                         '+  try {\n'
#                         '+    const user = await prisma.user.create({\n'
#                         '+      data: { name, email }\n'
#                         '+    });\n'
#                         '+    res.status(201).json(user);\n'
#                         '+  } catch (error) {\n'
#                         "+    res.status(500).json({ error: 'Failed to create "
#                         "user.' });\n"
#                         '+  }\n'
#                         '+});\n'
#                         '+\n'
#                         '+// GET /users/:id - get user by id\n'
#                         "+router.get('/users/:id', async (req: Request, res: "
#                         'Response) => {\n'
#                         '+  const id = Number(req.params.id);\n'
#                         '+  try {\n'
#                         '+    const user = await prisma.user.findUnique({\n'
#                         '+      where: { id },\n'
#                         '+    });\n'
#                         '+    if (user) {\n'
#                         '+      res.json(user);\n'
#                         '+    } else {\n'
#                         "+      res.status(404).json({ error: 'User not "
#                         "found.' });\n"
#                         '+    }\n'
#                         '+  } catch (error) {\n'
#                         "+    res.status(500).json({ error: 'Database error.' "
#                         '});\n'
#                         '+  }\n'
#                         '+});\n'
#                         '+\n'
#                         '+export default router;',
#                'sha': '8de9d96696dd2c1bdc5a0248129a6fb7c374aea7',
#                'status': 'added'}]]})

