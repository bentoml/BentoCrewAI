# BentoCrewAI: Serving CrewAI Agent with BentoML

Welcome to the BentoCrewAI project. This project demonstrates how to serve and deploy a [CrewAI](https://github.com/crewAIInc/crewAI) multi-agent application with the [BentoML](https://github.com/bentoml/BentoML) serving framework.


## Getting Started

This project is a reference implementation designed to be hackable. Download the source code and use it as a playground to build your own agent APIs:

Download source code:
```bash
git clone https://github.com/bentoml/BentoCrewAI.git
cd BentoCrewAI/src
```

Ensure you have Python >=3.10 <=3.13 installed on your system. Install dependencies:
```bash
# Create virtual env
pip install virtualenv
python -m venv venv
source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt --no-deps
```

Set your **`OPENAI_API_KEY`** environment variable:
```bash
export OPENAI_API_KEY='your_openai_key'
```


## Launching the API server

```bash
DEBUG=true ./venv/bin/bentoml serve bento_crew_demo.service:CrewAgent
```

## Calling the API

```bash
curl -X POST http://localhost:3000/run \
   -H 'Content-Type: application/json' \
   -d '{"topic": "BentoML"}'
```

The `/run` API endpoint takes the "topic" input from client, and returns the final results.

With the `DEBUG=true` env var, a `/debug` endpoint is also exposed for streaming all intermediate results from the Crew Agent for easier debugging:

```bash
curl -X POST http://localhost:3000/debug \
   -H 'Content-Type: application/json' \
   -d '{"topic": "Model Inference"}'
```

## Containerize 

Make sure you have Docker installed and running. Build a docker container image for deployment with BentoML:

```bash
bentoml build . --version dev
bentoml containerize crew_agent:dev
```

Follow CLI output instruction to run the generated container image. E.g.:

```bash
docker run --rm \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -e DEBUG=true \
    -p 3000:3000 \
    crew_agent:dev
```


## Customizing

Follow CrewAI docs on how to customize your Agents and tasks.

- Modify `src/bento_crew_demo/config/agents.yaml` to define your agents
- Modify `src/bento_crew_demo/config/tasks.yaml` to define your tasks
- Modify `src/bento_crew_demo/crew.py` to add your own logic, tools and specific args
- Modify `src/bento_crew_demo/main.py` to add custom inputs for your agents and tasks

## Using Open-Source LLMs

We recommend using [OpenLLM](https://github.com/bentoml/OpenLLM) on [BentoCloud](https://bentoml.com/)
for fast and efficient private LLM deployment:
```bash
# Install libraries
pip install -U openllm bentoml
openllm repo update

# Login/Signup BentoCloud
bentoml cloud login 

# Deploy mistral 7B
openllm deploy mistral:7b-4bit --instance-type gpu.t4.1.8x32
```
Follow CLI output instructions to view deployment details on BentoCloud UI, and copy your
deployed endpoint URL. 

> 💡 For other open-source LLMs, try running `openllm hello` command to explore more.

Next, add the following custom LLM definition to the `BentoCrewDemoCrew` class, replace with your deployed API endpoint URL:
```python
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, llm

@CrewBase
class BentoCrewDemoCrew():
    ...

    @llm
    def mistral(self) -> LLM:
        model_name="TheBloke/Mistral-7B-Instruct-v0.1-AWQ"
        return LLM(
            # add `openai/` prefix to model so litellm knows this is an openai
            # compatible endpoint and route to use OpenAI API Client
            model=f"openai/{model_name}",
			api_key="na",
            base_url="https://<YOUR_DEPLOYED_OPENLLM_ENDPOINT>/v1"
        )
```

And modify the `config/agent.yaml` file where you want to use this LLM, e.g.:

```diff
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.
+  llm: mistral
```


## Trouble shooting

BentoML 1.3.x requires opentelemetry-api==1.20.0 while CrewAI requires opentelemetry-api>=1.27.0; You may ignore the dependency resolver issue and proceed with the 1.27 version that CrewAi requires. BentoML team will update the package to support the newer version of opentelemetry libraries.


```bash
# Create virtual env
pip install virtualenv
python -m venv venv
source ./venv/bin/activate

# Install CrewAI after BentoML to override conflict dependency versions
pip install -U bentoml aiofiles
pip install -U crewai "crewai[tools]"

# Export dependencies list
pip freeze > requirements.txt
```

## Community

Join the [BentoML developer community](https://l.bentoml.com/join-slack) on Slack for more support and discussions!
