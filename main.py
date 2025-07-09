#!/usr/bin/env python

import os
import json
from pathlib import Path

from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

cwd = Path(__file__).parent
MODEL = "mistral-small-latest"  # or your preferred model
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise RuntimeError("Missing MISTRAL_API_KEY in environment")

client = Mistral(api_key)

def call_mistral(prompt, system_prompt):
    """
    Calls the Mistral API with the given prompt and system prompt.
    """
    response = client.chat.complete(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    print("Output: \n", response.choices[0].message.content)
    return response.choices[0].message.content

def alert_summariser_test():
    """
    Test function for alert summariser.
    """
    system_prompt = '''
    You are an observability alerting assistant. 
    Summarise the input alert or incident information into a clear, concise, and non-technical paragraph suitable for an engineer to quickly understand the issue, its impact, and urgency.
    '''
    complex_alert = {
        "alert_name": "High CPU Usage",
        "severity": "critical",
        "description": "CPU usage has exceeded 90% for the last 5 minutes on server XYZ. This could indicate a potential performance issue or a runaway process.",
        "timestamp": "2023-10-01T12:00:00Z",
        "application": "web-server",
        "environment": "production"
    }
    prompt = f'''Alert Details: {json.dumps(complex_alert, indent=2)}'''
    print('Prompt:', prompt)
    result = call_mistral(prompt, system_prompt)
    with open(cwd / 'examples/alert_summariser.txt', 'w') as f:
        f.write(f"Prompt:\n {prompt}\n")
        f.write("\nOutput:\n")
        f.write(result)

def clickhouse_query_generator():
    """
    Test function for clickhouse query language generator.
    """
    system_prompt = '''
    You are an observability Clickhouse Query Generator. Convert the given prompt into a valid Clickhouse Query (CQL). The query should be optimized and syntactically correct.
    
    Provide the answer in Clickhouse Query format:
    ```cql ```
    '''
    prompt = "What is the average response time for the last 24 hours?"
    print('Prompt: ', prompt)
    result = call_mistral(prompt, system_prompt)
    with open(cwd / 'examples/clickhouse_query_generator.txt', 'w') as f:
        f.write(f"Prompt:\n{prompt}\n")
        f.write("\nOutput:\n")
        f.write(result)

def grafana_dashboard_generator():
    """
    Test function for grafana dashboard generator.
    """
    system_prompt = '''
    Analyse the input Prometheus query and generate a grafana dashboard json code with various panels associated with different metrics that you think are necessary to be tracked. Group related metrics together and use appropriate types of panels - gauges, text, histograms etc. - based on your analysis of the metrics.

    Provide the answer in JSON format:
    ```json```
    '''
    complex_query = 'sum(rate(http_requests_total{job="web-server", status="500"}[5m])) by (instance)'
    prompt = f'''Prometheus Query: {complex_query}'''
    print('Prompt: ', prompt)
    result = call_mistral(prompt, system_prompt)

    with open(cwd / 'examples/grafana_dashboard_generator.txt', 'w') as f:
        f.write(f"Prompt:\n{prompt}\n")
        f.write("\nOutput:\n")
        f.write(result)

def log_filter():
    """
    Test function for log filtering.
    """
    system_prompt = '''
    You are a log parsing assistant. From the following raw log entries, extract the key information such as timestamp, log level, error messages, and any identifiers like request IDs or user IDs. Return the extracted data in JSON format with appropriate fields.

    Provide the answer in JSON format:
    ```json ```
    '''
    raw_logs = """
2023-10-01 12:00:00 INFO [web-server] Request received
2023-10-01 12:00:01 ERROR [web-server] Failed to connect to database
2023-10-01 12:00:02 INFO [web-server] Response sent
2023-10-01 12:00:03 WARN [database] High memory usage detected
2023-10-01 12:00:04 ERROR [database] Timeout while processing request
"""
    prompt = f'''Please help me extract key metadata from the following raw logs: {raw_logs}'''
    print('Prompt: ', prompt)
    result = call_mistral(prompt, system_prompt)

    with open(cwd / 'examples/log_filter.txt', 'w') as f:
        f.write(f"Prompt:\n{prompt}\n")
        f.write("\nOutput:\n")
        f.write(result)

def onboarding_guide():
    """
    Test function for guiding teams on onboarding to observability.
    """
    with open(cwd / 'dummy_wiki.md', 'r') as f:
        wiki = f.read()

    system_prompt = f'''You are an onboarding guide for Team Observability. You help teams understand how to onboard to observability practices, tools, and processes based on the documented wiki below:
    {wiki}'''

    prompts = ["Please provide me a contact for your team.",
                "Please provide a me a brief overview of your team and its responsibilities.",
                "Please provide a step-by-step guide on how to onboard to your observability system."]
    
    with open(cwd / 'examples/onboarding_guide.txt', 'w') as f:
        f.close() # Clear the file before writing

    for prompt in prompts:
        print('Prompt: ', prompt)
        result = call_mistral(prompt, system_prompt)
        with open(cwd / 'examples/onboarding_guide.txt', 'a') as f:
            f.write(f"\nPrompt:\n{prompt}\n")
            f.write("\nOutput:\n")
            f.write(result)

def prometheus_config_generator():
    """
    Test function for prometheus configruation generator.
    """
    system_prompt = '''
    You are an observability Prometheus Configuration Generator. Generate a suitable Prometheus custom job definition from the given prompt. The job should be well-structured and include necessary fields like job name, scrape interval, and target endpoints.
    Provide the answer in Prometheus yml format:
    ```cql ```
    '''
    prompt = '''Generate a Prometheus job configuration for scraping metrics from 3 web servers, each running on port 8080, labeled as 'web-server-1', 'web-server-2', and 'web-server-3'.
    These servers are discoverable via HTTP Service Discovery at http://web-server-discovery/targets.
    The scrape interval should be 10 seconds.'''
    print('Prompt: ', prompt)
    result = call_mistral(prompt, system_prompt)
    with open(cwd / 'examples/prometheus_config_generator.txt', 'w') as f:
        f.write(f"Prompt:\n{prompt}\n")
        f.write("\nOutput:\n")
        f.write(result)

def review_infra_code():
    """
    Test function for reviewing infrastructure code.
    """
    system_prompt = '''You are an observability deployment code reviewer. Review the given infrastructure code and try to spot any syntax errors/issues.
    You can provide your analysis in the following format:
    1. Summary
    2. Recommended change in a single content block if applicable. '''
    with open(cwd / 'incorrect_k8_deployment.yaml', 'r') as f:
        infra_code = f.read()

    prompt = f'''Review the following infrastructure code for K8 Deployment:
    ```yaml
    {infra_code}
    ```'''
    print('Prompt: ', prompt)
    result = call_mistral(prompt, system_prompt)
    with open(cwd / 'examples/review_infra_code.txt', 'w') as f:
        f.write(f"Prompt:\n{prompt}\n")
        f.write("\nOutput:\n")
        f.write(result)

def rca_assistant():
    """
    Test function for Root Cause Analysis assistant.
    """
    system_prompt = '''
    You are an observability and incident response assistant.
    Given the observabilty data, analyze the root cause of the incident. 
    Provide a short RCA summary including:
    - What is likely causing the issue
    - What systems are affected
    - Suggested next steps to mitigate or resolve
    '''

    with open(cwd / 'observability_data.json', 'r') as f:
        obs_data = f.read()

    prompt = f'''```json{obs_data}```'''
    print('Prompt: ', prompt)
    result = call_mistral(prompt, system_prompt)
    with open(cwd / 'examples/rca_assistant.txt', 'w') as f:
        f.write(f"Prompt:\n{prompt}\n")
        f.write("\nOutput:\n")
        f.write(result)

print(f'############ Start ############\n')

funcs = [
    alert_summariser_test,
    grafana_dashboard_generator,
    log_filter,
    clickhouse_query_generator,
    prometheus_config_generator,
    review_infra_code,
    onboarding_guide,
    rca_assistant
]

for func in funcs:
    print(f'------------------------ Running {func.__name__} ------------------------')
    func()
    print('\n')

print(f'############ End ############\n')