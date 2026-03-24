#!/usr/bin/env python3
"""
BlackRoad Agent Router
Routes user messages to the best-matching agent based on intent detection.
Uses keyword and pattern matching -- no ML dependencies required.
"""

import re
import sys
import json
from collections import defaultdict

INTENT_MAP = {
    "code": {
        "agent": "coder",
        "keywords": [
            "code", "script", "function", "class", "module", "refactor",
            "implement", "build", "program", "compile", "debug", "fix bug",
            "syntax", "api", "endpoint", "server", "client", "library",
            "import", "package", "deploy code", "pull request", "commit",
            "python", "javascript", "rust", "bash", "html", "css", "sql",
            "node", "react", "typescript", "dockerfile", "yaml", "json"
        ],
        "patterns": [
            r"write\s+(a\s+)?(\w+\s+)?(script|function|class|program|module)",
            r"(fix|debug|patch)\s+(the\s+)?(bug|error|issue|crash)",
            r"how\s+do\s+I\s+(code|implement|build|write)",
            r"generate\s+(a\s+)?(code|script|function)",
        ]
    },
    "research": {
        "agent": "scholar",
        "keywords": [
            "research", "explain", "what is", "how does", "why does",
            "compare", "difference between", "history of", "define",
            "analyze", "investigate", "study", "paper", "source",
            "evidence", "reference", "citation", "literature", "theory",
            "concept", "principle", "framework", "methodology"
        ],
        "patterns": [
            r"(what|how|why)\s+(is|does|did|are|was|were)\s+",
            r"explain\s+(how|what|why|the)",
            r"(compare|contrast)\s+\w+\s+(and|vs|versus|with)",
            r"tell\s+me\s+about",
        ]
    },
    "math": {
        "agent": "pascal",
        "keywords": [
            "math", "calculate", "equation", "formula", "proof",
            "theorem", "prime", "integral", "derivative", "matrix",
            "algebra", "geometry", "calculus", "statistics", "probability",
            "amundson", "constant", "factorial", "fibonacci", "sequence",
            "number theory", "combinatorics", "graph theory"
        ],
        "patterns": [
            r"(solve|compute|calculate|evaluate)\s+",
            r"(prove|show)\s+that",
            r"\d+\s*[\+\-\*\/\^]\s*\d+",
            r"(what|find)\s+(is\s+)?(the\s+)?(sum|product|integral|derivative|limit)",
        ]
    },
    "write": {
        "agent": "writer",
        "keywords": [
            "write", "draft", "compose", "blog", "article", "post",
            "copy", "content", "documentation", "readme", "guide",
            "tutorial", "email", "letter", "report", "summary",
            "changelog", "release notes", "announcement", "tagline"
        ],
        "patterns": [
            r"write\s+(a\s+)?(blog|article|post|email|letter|report|doc)",
            r"draft\s+(a\s+)?(message|email|announcement|response)",
            r"(summarize|rewrite|edit)\s+(this|the)",
        ]
    },
    "security": {
        "agent": "cipher",
        "keywords": [
            "security", "vulnerability", "exploit", "attack", "encrypt",
            "decrypt", "hash", "token", "secret", "credential", "password",
            "firewall", "iptables", "ssl", "tls", "certificate", "audit",
            "permission", "access control", "authentication", "authorization",
            "zero trust", "scan", "pentest", "hardening"
        ],
        "patterns": [
            r"(scan|check|audit)\s+(for\s+)?(vulnerabilit|secret|credential|security)",
            r"(encrypt|decrypt|hash|sign|verify)\s+",
            r"(secure|harden|lock\s+down)\s+",
            r"is\s+(this|it)\s+(safe|secure|vulnerable)",
        ]
    },
    "teach": {
        "agent": "tutor",
        "keywords": [
            "teach", "learn", "understand", "lesson", "course",
            "beginner", "introduction", "getting started", "how to start",
            "onboard", "walkthrough", "step by step", "for beginners",
            "new to", "first time", "basics", "fundamentals"
        ],
        "patterns": [
            r"(teach|show)\s+me\s+(how\s+to|about)",
            r"I('m|\s+am)\s+(new|a\s+beginner|learning|starting)",
            r"(help\s+me\s+)?(understand|learn|get\s+started)",
        ]
    },
    "network": {
        "agent": "alice",
        "keywords": [
            "network", "dns", "nginx", "proxy", "gateway", "router",
            "port", "ip", "subnet", "ping", "traceroute", "latency",
            "bandwidth", "uptime", "pi-hole", "redis", "cache",
            "qdrant", "vector", "postgres", "database"
        ],
        "patterns": [
            r"(check|test|verify)\s+(the\s+)?(network|connection|dns|proxy)",
            r"(why|is)\s+.*(down|unreachable|slow|timeout)",
            r"(configure|setup|add)\s+(a\s+)?(dns|proxy|route|domain)",
        ]
    },
    "inference": {
        "agent": "cecilia",
        "keywords": [
            "model", "ollama", "inference", "embedding", "vector",
            "minio", "storage", "bucket", "hailo", "npu", "gpu",
            "tensor", "neural", "training", "fine-tune", "quantize",
            "llama", "codellama", "mistral", "weights"
        ],
        "patterns": [
            r"(run|load|switch|pull)\s+(a\s+)?(model|ollama)",
            r"(store|upload|download)\s+(to|from)\s+minio",
            r"(embed|vectorize|encode)\s+",
        ]
    },
    "devops": {
        "agent": "octavia",
        "keywords": [
            "deploy", "docker", "container", "gitea", "ci", "cd",
            "pipeline", "worker", "nats", "message queue", "build",
            "release", "rollback", "staging", "production", "helm",
            "kubernetes", "systemd", "service", "daemon"
        ],
        "patterns": [
            r"(deploy|ship|release|push)\s+(to\s+)?(production|staging|octavia)",
            r"(start|stop|restart)\s+(the\s+)?(container|service|worker|daemon)",
            r"(create|setup|configure)\s+(a\s+)?(pipeline|workflow|action)",
        ]
    },
    "monitoring": {
        "agent": "aria",
        "keywords": [
            "monitor", "alert", "metric", "dashboard", "status",
            "health", "uptime", "downtime", "log", "trace",
            "influxdb", "grafana", "headscale", "vpn", "tunnel",
            "cloudflare", "watchdog", "heartbeat"
        ],
        "patterns": [
            r"(show|check|get)\s+(the\s+)?(status|health|metrics|logs)",
            r"(set\s+up|create)\s+(an?\s+)?(alert|monitor|dashboard)",
            r"(is|are)\s+.*(running|alive|healthy|up)",
        ]
    },
    "hosting": {
        "agent": "lucidia",
        "keywords": [
            "website", "site", "hosting", "nginx config", "web app",
            "powerdns", "actions runner", "static site", "html page",
            "subdomain", "reverse proxy site", "web server"
        ],
        "patterns": [
            r"(host|serve|publish)\s+(a\s+)?(website|site|page|app)",
            r"(add|create|setup)\s+(a\s+)?(subdomain|site|vhost)",
        ]
    },
    "coordinate": {
        "agent": "road",
        "keywords": [
            "status", "fleet", "all agents", "coordinate", "priority",
            "roadmap", "plan", "strategy", "assign", "delegate",
            "overview", "summary", "report", "briefing"
        ],
        "patterns": [
            r"(give\s+me|show|what('s|\s+is))\s+(the\s+)?(status|overview|summary|briefing)",
            r"(assign|delegate|route)\s+(this|it)\s+to",
            r"(which|what)\s+agent\s+(should|can|would)",
        ]
    }
}


def tokenize(text):
    """Lowercase and split text into tokens."""
    return re.findall(r'[a-z0-9]+', text.lower())


def score_intent(message, intent_config):
    """Score how well a message matches an intent. Returns 0.0-1.0."""
    msg_lower = message.lower()
    tokens = tokenize(message)
    score = 0.0

    # Keyword matching (each keyword hit adds to score)
    keyword_hits = 0
    for keyword in intent_config["keywords"]:
        if keyword in msg_lower:
            keyword_hits += 1
            # Multi-word keywords are more specific, worth more
            if " " in keyword:
                keyword_hits += 1

    if intent_config["keywords"]:
        keyword_score = min(keyword_hits / 3.0, 1.0)
        score += keyword_score * 0.6

    # Pattern matching (regex patterns are high-signal)
    pattern_hits = 0
    for pattern in intent_config["patterns"]:
        if re.search(pattern, msg_lower):
            pattern_hits += 1

    if intent_config["patterns"]:
        pattern_score = min(pattern_hits / 2.0, 1.0)
        score += pattern_score * 0.4

    return round(min(score, 1.0), 3)


def route(message):
    """
    Route a message to the best-matching agent.

    Returns dict with:
        agent: agent ID
        intent: detected intent category
        confidence: 0.0-1.0 confidence score
        alternatives: list of other possible matches
    """
    if not message or not message.strip():
        return {
            "agent": "road",
            "intent": "coordinate",
            "confidence": 0.0,
            "alternatives": []
        }

    scores = {}
    for intent_name, config in INTENT_MAP.items():
        score = score_intent(message, config)
        if score > 0:
            scores[intent_name] = {
                "agent": config["agent"],
                "score": score
            }

    if not scores:
        return {
            "agent": "road",
            "intent": "coordinate",
            "confidence": 0.1,
            "alternatives": []
        }

    # Sort by score descending
    ranked = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
    best_intent, best_match = ranked[0]

    alternatives = []
    for intent_name, match in ranked[1:4]:
        if match["score"] > 0.1:
            alternatives.append({
                "agent": match["agent"],
                "intent": intent_name,
                "confidence": match["score"]
            })

    return {
        "agent": best_match["agent"],
        "intent": best_intent,
        "confidence": best_match["score"],
        "alternatives": alternatives
    }


def main():
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = input("Enter message: ").strip()

    result = route(message)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
