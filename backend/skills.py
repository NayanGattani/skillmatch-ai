# Technical skills database - organized by category
TECH_SKILLS = {
    "languages": [
        "Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript",
        "C#", "PHP", "Ruby", "Kotlin"
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