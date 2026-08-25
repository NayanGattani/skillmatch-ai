import re

# Technical skills database - organized by category
TECH_SKILLS = {
    "languages": [
        "Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript",
        "C#", "PHP", "Ruby", "Kotlin", "C"
    ],
    "databases": [
        "SQL", "PostgreSQL", "MongoDB", "Redis", "MySQL", "DynamoDB",
        "Elasticsearch", "Cassandra", "SQLite"
    ],
    "cloud": [
        "AWS", "GCP", "Azure", "EC2", "S3", "Lambda", "RDS",
        "CloudFormation", "IAM"
    ],
    "tools": [
        "Docker", "Kubernetes", "Git", "Jenkins", "Terraform",
        "Ansible", "Vagrant"
    ],
    "frontend": [
        "React", "Vue", "Angular", "HTML", "CSS", "Tailwind",
        "Next.js", "Webpack", "Vite"
    ],
    "backend": [
        "FastAPI", "Django", "Flask", "Node.js", "Express",
        "Spring Boot", "Spring", "Rails", "ASP.NET"
    ],
    "data": [
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Spark", "Hadoop",
        "Matplotlib", "Tableau", "Power BI"
    ],
    "devops": [
        "CI/CD", "Linux", "Bash", "Shell", "Nginx", "Apache",
        "Grafana", "Prometheus", "ELK"
    ],
    "testing": [
        "Unit Testing", "Integration Testing", "Jest", "Pytest",
        "Selenium", "Cypress", "Junit"
    ],
    "concepts": [
        "REST API", "GraphQL", "Microservices", "System Design",
        "OOP", "SOLID", "Design Patterns", "Distributed Systems",
        "Load Balancing", "Caching", "Message Queues"
    ],
    "messaging": [
        "RabbitMQ", "Kafka", "ActiveMQ", "SQS", "SNS", "Pub/Sub"
    ]
}


# Flatten into one searchable list
ALL_SKILLS = []

for category in TECH_SKILLS.values():
    ALL_SKILLS.extend(category)


# Every variant points to one canonical skill.
# The extractor searches these variants, but returns only
# the canonical skill name.
SKILL_ALIASES = {
    # Kubernetes
    "k8s": "Kubernetes",
    "k8": "Kubernetes",

    # PostgreSQL
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "psql": "PostgreSQL",

    # React
    "react.js": "React",
    "reactjs": "React",
    "react.ts": "React",

    # Node
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    # Google Cloud
    "google cloud": "GCP",
    "google cloud platform": "GCP",

    # C variants
    "c#": "C#",
    "c++": "C++",

    # CI/CD
    "ci cd": "CI/CD",

    # REST
    "rest": "REST API",
    "restful": "REST API",
    "rest api": "REST API",
    "rest apis": "REST API",

    # Testing
    "unit test": "Unit Testing",
    "integration test": "Integration Testing",
}


def normalize_skill(skill: str) -> str:
    """
    Convert a skill variant into its canonical skill name.
    """

    skill_lower = skill.lower().strip()

    if skill_lower in SKILL_ALIASES:
        return SKILL_ALIASES[skill_lower]

    for canonical in ALL_SKILLS:
        if canonical.lower() == skill_lower:
            return canonical

    return skill