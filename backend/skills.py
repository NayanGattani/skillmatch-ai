# Common technical skills database
TECH_SKILLS = {
    "languages": ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"],
    "databases": ["SQL", "PostgreSQL", "MongoDB", "Redis", "MySQL", "DynamoDB"],
    "cloud": ["AWS", "GCP", "Azure", "EC2", "S3", "Lambda", "RDS"],
    "tools": ["Docker", "Kubernetes", "Git", "Jenkins", "Terraform"],
    "frontend": ["React", "Vue", "Angular", "HTML", "CSS", "Tailwind"],
    "backend": ["FastAPI", "Django", "Flask", "Node.js", "Express"],
    "data": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Spark", "Hadoop"],
}

# Flatten into one searchable list
ALL_SKILLS = []
for category in TECH_SKILLS.values():
    ALL_SKILLS.extend(category)