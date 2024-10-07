import os
import asyncio
import aiofiles
from contextlib import redirect_stdout
from typing import AsyncGenerator

import bentoml
from pydantic import Field

from bento_crew_demo.crew import BentoCrewDemoCrew

DEBUG = os.environ.get("DEBUG", False)

@bentoml.service(
    workers=1,
    resources={
        "cpu": "2000m"
    },
    traffic={
        "concurrency": 16,
        "external_queue": True
    }
)
class CrewAgent:

    @bentoml.task
    def run(self, topic: str = Field(default="LLM Agent")) -> str:
        return BentoCrewDemoCrew().crew().kickoff(inputs={"topic": topic}).raw

    # Whether to expose the /debug endpoint which streams the full Crew output to the
    # client side, including all intermediate steps. Use DEBUG=True to enable, e.g.:
    # `DEBUG=true bentoml serve bento_crew_demo.service:CrewAgent`
    if DEBUG:
        @bentoml.api
        async def debug(
            self, topic: str = Field(default="LLM Agent")
        ) -> AsyncGenerator[str, None]:
            read_fd, write_fd = os.pipe()

            async def kickoff():
                with os.fdopen(write_fd, "w", buffering=1) as write_file:
                    with redirect_stdout(write_file):
                        await BentoCrewDemoCrew().crew().kickoff_async(
                            inputs={"topic": topic}
                        )

            asyncio.create_task(kickoff())

            # Yield CrewAgent logs as they are written to the pipe
            async with aiofiles.open(read_fd, mode='r') as read_file:
                async for line in read_file:
                    if not line:
                        break
                    yield line