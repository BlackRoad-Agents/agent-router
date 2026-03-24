# agent-router

Intent-based agent routing for BlackRoad OS. Takes a user message and returns the best-matching agent.

## What This Is

A Python routing engine that parses user messages for intent using keyword matching and regex patterns. No ML dependencies -- runs anywhere with Python 3.6+. Maps 12 intent categories to 12 agents across the fleet.

## Usage

```bash
# Command line
python3 router.py "Write a Python script to scan open ports"
# Output: {"agent": "coder", "intent": "code", "confidence": 0.8, "alternatives": [...]}

python3 router.py "Is the network down?"
# Output: {"agent": "alice", "intent": "network", "confidence": 0.6, ...}

# Interactive
python3 router.py
# Enter message: teach me about WireGuard
# Output: {"agent": "tutor", "intent": "teach", "confidence": 0.6, ...}
```

```python
# As a module
from router import route

result = route("Deploy the new worker to production")
print(result["agent"])      # "octavia"
print(result["confidence"]) # 0.6
```

## Intent Categories

| Intent | Agent | Triggers |
|--------|-------|----------|
| code | coder | code, script, function, build, debug |
| research | scholar | explain, what is, compare, analyze |
| math | pascal | calculate, prove, equation, theorem |
| write | writer | draft, blog, documentation, email |
| security | cipher | vulnerability, encrypt, audit, scan |
| teach | tutor | learn, beginner, getting started |
| network | alice | dns, proxy, port, ping, latency |
| inference | cecilia | model, ollama, embedding, tensor |
| devops | octavia | deploy, docker, pipeline, gitea |
| monitoring | aria | status, alert, metric, health |
| hosting | lucidia | website, hosting, subdomain |
| coordinate | road | fleet, all agents, priority, plan |

## Response Format

```json
{
  "agent": "coder",
  "intent": "code",
  "confidence": 0.8,
  "alternatives": [
    {"agent": "octavia", "intent": "devops", "confidence": 0.2}
  ]
}
```

Messages that match no intent default to Road (fleet commander) for triage.

Part of BlackRoad-Agents. Remember the Road. Pave Tomorrow. Incorporated 2025.
