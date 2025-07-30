import os
import requests

ENV_AAP_HOST = "AAP_HOST"
ENV_AAP_TOKEN = "AAP_TOKEN"

def run_ansible_template(template):

  # gather configuration
  if ENV_AAP_HOST not in os.environ:
    raise ValueError("AAP Host is a required configuration parameter")
  host = os.environ[ENV_AAP_HOST]
  if host is None or len(host) == 0:
    raise ValueError("AAP Host is defined but is empty.")
  if ENV_AAP_TOKEN not in os.environ:
    raise ValueError("AAP Token is a required configuration parameter")
  token = os.environ[ENV_AAP_TOKEN]
  if token is None or len(token) == 0:
    raise ValueError("AAP Token is defined but is empty.")

  # Setup headers
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {token}",
  }

  # Setup data
  data = {}

  # make invocation
  response = requests.post(host + "/api/controller/v2/job_templates/" + template + "/launch/",
                           json=data,
                           headers=headers)
  response.raise_for_status()
  print(response)
