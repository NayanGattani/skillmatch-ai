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

# Skill aliases - map variations to canonical names
SKILL_ALIASES = {
    # Kubernetes variants
    "k8s": "Kubernetes",
    "k8": "Kubernetes",
    
    # PostgreSQL variants
    "postgres": "PostgreSQL",
    "psql": "PostgreSQL",
    
    # React variants
    "react.js": "React",
    "reactjs": "React",
    "react.ts": "React",
    
    # Node variants
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    
    # Google Cloud
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    
    # C variants
    "c#": "C#",
    "c++": "C++",
    
    # CI/CD variants
    "ci cd": "CI/CD",
    
    # REST variants
    "restful": "REST API",
    "rest": "REST API",
    "rest apis":"REST API",
    
    # Testing variants
    "unit test": "Unit Testing",
    "integration test": "Integration Testing",
}

def normalize_skill(skill: str) -> str:
    """
    Normalize a skill name using aliases.
    Returns canonical skill name from ALL_SKILLS.
    """
    skill_lower = skill.lower().strip()
    
    # Check if it's in aliases
    if skill_lower in SKILL_ALIASES:
        return SKILL_ALIASES[skill_lower]
    
    # Check if it's already canonical
    for canonical in ALL_SKILLS:
        if canonical.lower() == skill_lower:
            return canonical
    
    # Not found
    return skill