"""Broad, occupation-agnostic competency vocabulary and normalization helpers."""
from __future__ import annotations
import re

COMPETENCY_GROUPS = {
"technology": ["Python","JavaScript","Java","C++","Go","Rust","TypeScript","C#","PHP","Ruby","Kotlin","C","SQL","PostgreSQL","MongoDB","Redis","MySQL","DynamoDB","Elasticsearch","Cassandra","SQLite","AWS","GCP","Azure","EC2","S3","Lambda","RDS","Docker","Kubernetes","Git","Jenkins","Terraform","Ansible","Linux","Bash","Nginx","React","Vue","Angular","HTML","CSS","Tailwind","Next.js","Vite","FastAPI","Django","Flask","Node.js","Express","Spring Boot","Spring","Rails","ASP.NET","Pandas","NumPy","Scikit-learn","TensorFlow","PyTorch","Spark","Hadoop","Tableau","Power BI","CI/CD","REST API","GraphQL","Microservices","System Design","OOP","SOLID","Kafka","RabbitMQ","SQS","SNS","Jira","Confluence","Unit Testing","Integration Testing","Pytest","Jest","Selenium","Figma","GitHub","GitLab","Bitbucket","Salesforce","SAP","Oracle","Excel","PowerPoint","Word","Google Analytics","Google Ads","HubSpot","Adobe Creative Suite","AutoCAD","SolidWorks","MATLAB","Simulink"],
"business": ["financial modeling","financial analysis","valuation","forecasting","budgeting","financial reporting","accounting","bookkeeping","FP&A","audit","taxation","risk management","compliance","procurement","supply chain","inventory management","operations management","project management","program management","product management","business analysis","market research","competitive analysis","strategy","business development","sales","account management","customer success","customer relationship management","stakeholder management","vendor management","change management","process improvement","process optimization","quality assurance","quality control","data analysis","data visualization","reporting","performance management","KPI management","requirements gathering","documentation","contract negotiation","vendor management"],
"marketing": ["SEO","SEM","content marketing","content strategy","copywriting","social media marketing","email marketing","campaign management","brand management","digital marketing","market segmentation","lead generation","conversion optimization","A/B testing","public relations","communications","community management","marketing analytics","advertising"],
"people": ["recruiting","talent acquisition","employee relations","performance management","learning and development","training","workforce planning","compensation","benefits administration","human resources","HRIS","onboarding","interviewing"],
"engineering": ["mechanical design","product design","CAD","GD&T","finite element analysis","FEA","manufacturing","machining","prototyping","3D printing","electrical design","circuit design","PCB design","embedded systems","PLC","control systems","civil engineering","structural analysis","construction management","BIM","Revit","surveying"],
"healthcare": ["patient care","clinical research","clinical documentation","medical coding","healthcare administration","patient assessment","case management","care coordination","HIPAA","EMR","EHR","phlebotomy","medication administration"],
"research": ["research methodology","literature review","experimental design","statistical analysis","qualitative research","quantitative research","survey design","data collection","academic writing","technical writing","scientific writing","publications","peer review","research ethics","SPSS","R","Stata","SAS"],
"design": ["UI design","UX design","user research","interaction design","visual design","graphic design","prototyping","wireframing","design systems","information architecture","usability testing","accessibility","typography","branding"],
"legal": ["legal research","contract drafting","contract review","litigation","case management","regulatory compliance","due diligence","legal writing","negotiation","dispute resolution","corporate law","intellectual property"],
"education": ["curriculum development","lesson planning","classroom management","instructional design","assessment design","student advising","academic advising","teaching","facilitation","training delivery","e-learning"],
"languages": ["English","Hindi","Spanish","French","German","Mandarin","Arabic","Japanese","Portuguese","Tamil","Telugu"],
}
TECH_SKILLS = COMPETENCY_GROUPS
ALL_SKILLS = [x for group in COMPETENCY_GROUPS.values() for x in group]
SKILL_ALIASES = {
"k8s":"Kubernetes","k8":"Kubernetes","postgres":"PostgreSQL","postgresql":"PostgreSQL","psql":"PostgreSQL",
"react.js":"React","reactjs":"React","node":"Node.js","nodejs":"Node.js","node.js":"Node.js","google cloud":"GCP","google cloud platform":"GCP",
"ci cd":"CI/CD","ci-cd":"CI/CD","rest":"REST API","restful":"REST API","rest api":"REST API","rest apis":"REST API","restful api":"REST API","restful apis":"REST API","restful services":"REST API","web api":"REST API",
"unit test":"Unit Testing","unit tests":"Unit Testing","integration test":"Integration Testing","integration tests":"Integration Testing","microsoft excel":"Excel","ms excel":"Excel","adobe creative cloud":"Adobe Creative Suite",
"fp&a":"FP&A","financial planning and analysis":"FP&A","financial models":"financial modeling","forecasts":"forecasting","forecast":"forecasting","stakeholder relationships":"stakeholder management","lesson plans":"lesson planning","lesson planning":"lesson planning","classroom management":"classroom management","managed classrooms":"classroom management","classroom":"classroom management","search engine optimization":"SEO","search engine marketing":"SEM","user experience":"UX design","user interface":"UI design","finite element analysis":"FEA","electronic medical record":"EMR","electronic health record":"EHR","key performance indicators":"KPI management","vendor relationships":"vendor management","supplier management":"vendor management","manage vendors":"vendor management","vendor relations":"vendor management",
}

def _norm_key(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9+#&./-]+", " ", value.lower())).strip()

_ALIAS_KEYS = {_norm_key(k): v for k,v in SKILL_ALIASES.items()}
_CANONICAL_KEYS = {_norm_key(x): x for x in ALL_SKILLS}

def normalize_skill(skill: str) -> str:
    key = _norm_key(skill)
    return _ALIAS_KEYS.get(key, _CANONICAL_KEYS.get(key, skill.strip()))

def aliases_for(canonical: str) -> set[str]:
    canonical = normalize_skill(canonical)
    return {canonical} | {a for a,t in SKILL_ALIASES.items() if normalize_skill(t)==canonical}
