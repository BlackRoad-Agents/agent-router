<!-- BlackRoad SEO Enhanced -->

# agent router

> Part of **[BlackRoad OS](https://blackroad.io)** — Sovereign Computing for Everyone

[![BlackRoad OS](https://img.shields.io/badge/BlackRoad-OS-ff1d6c?style=for-the-badge)](https://blackroad.io)
[![BlackRoad Agents](https://img.shields.io/badge/Org-BlackRoad-Agents-2979ff?style=for-the-badge)](https://github.com/BlackRoad-Agents)
[![License](https://img.shields.io/badge/License-Proprietary-f5a623?style=for-the-badge)](LICENSE)

**agent router** is part of the **BlackRoad OS** ecosystem — a sovereign, distributed operating system built on edge computing, local AI, and mesh networking by **BlackRoad OS, Inc.**

## About BlackRoad OS

BlackRoad OS is a sovereign computing platform that runs AI locally on your own hardware. No cloud dependencies. No API keys. No surveillance. Built by [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc), a Delaware C-Corp founded in 2025.

### Key Features
- **Local AI** — Run LLMs on Raspberry Pi, Hailo-8, and commodity hardware
- **Mesh Networking** — WireGuard VPN, NATS pub/sub, peer-to-peer communication
- **Edge Computing** — 52 TOPS of AI acceleration across a Pi fleet
- **Self-Hosted Everything** — Git, DNS, storage, CI/CD, chat — all sovereign
- **Zero Cloud Dependencies** — Your data stays on your hardware

### The BlackRoad Ecosystem
| Organization | Focus |
|---|---|
| [BlackRoad OS](https://github.com/BlackRoad-OS) | Core platform and applications |
| [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc) | Corporate and enterprise |
| [BlackRoad AI](https://github.com/BlackRoad-AI) | Artificial intelligence and ML |
| [BlackRoad Hardware](https://github.com/BlackRoad-Hardware) | Edge hardware and IoT |
| [BlackRoad Security](https://github.com/BlackRoad-Security) | Cybersecurity and auditing |
| [BlackRoad Quantum](https://github.com/BlackRoad-Quantum) | Quantum computing research |
| [BlackRoad Agents](https://github.com/BlackRoad-Agents) | Autonomous AI agents |
| [BlackRoad Network](https://github.com/BlackRoad-Network) | Mesh and distributed networking |
| [BlackRoad Education](https://github.com/BlackRoad-Education) | Learning and tutoring platforms |
| [BlackRoad Labs](https://github.com/BlackRoad-Labs) | Research and experiments |
| [BlackRoad Cloud](https://github.com/BlackRoad-Cloud) | Self-hosted cloud infrastructure |
| [BlackRoad Forge](https://github.com/BlackRoad-Forge) | Developer tools and utilities |

### Links
- **Website**: [blackroad.io](https://blackroad.io)
- **Documentation**: [docs.blackroad.io](https://docs.blackroad.io)
- **Chat**: [chat.blackroad.io](https://chat.blackroad.io)
- **Search**: [search.blackroad.io](https://search.blackroad.io)

---


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
