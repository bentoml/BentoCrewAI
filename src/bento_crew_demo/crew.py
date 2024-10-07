from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, llm

# Uncomment the following line to use an example of a custom tool
# from bento_crew_demo.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class BentoCrewDemoCrew():
	"""BentoCrewDemo crew"""
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	# # Uncomment the code below for using private deployed open-source LLM
	# @llm
	# def mistral(self) -> LLM:
	# 	model_name="TheBloke/Mistral-7B-Instruct-v0.1-AWQ"
	# 	return LLM(
    #         # add `openai/` prefix to model so litellm knows this is an openai
    #         # compatible endpoint and route to use OpenAI API Client
    #         model=f"openai/{model_name}",
	# 		api_key="na",
    #         base_url="https://<YOUR_DEPLOYED_OPENLLM_ENDPOINT>/v1"
    #     )

	@crew
	def crew(self) -> Crew:
		"""Creates the BentoCrewDemo crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)