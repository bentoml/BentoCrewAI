# BentoCrewDemo Crew

Welcome to the BentoCrewAI demo project. This template is designed to help you serve and deploy a CrewAI multi-agent application with the BentoML serving framework. This project


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

Build a docker container image for deployment with BentoML:

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
