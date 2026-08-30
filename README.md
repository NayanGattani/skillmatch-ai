# SkillMatch AI

**AI-powered resume–job matching and analysis platform.**

SkillMatch analyzes a candidate's resume against a target job description and provides an ATS-style compatibility assessment, skill matching, missing-skill identification, and AI-generated recommendations.

**Live Demo:** [http://15.252.174.56](http://15.252.174.56)

---

## Overview

Finding out whether a resume actually matches a job description usually involves manually comparing requirements, skills, and experience.

SkillMatch automates that process.

A user uploads a resume, provides a job description, and receives a structured analysis of how well the resume aligns with the role.

### What it does

* Resume analysis
* Job-description analysis
* ATS-style compatibility scoring
* Matched skill identification
* Missing skill identification
* AI-powered recommendations
* Resume storage using Amazon S3
* Persistent application data using PostgreSQL

---

## Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         │  Browser / Mobile   │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP :80
                                    ▼
                         ┌─────────────────────┐
                         │       Nginx         │
                         │    Reverse Proxy    │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │  TanStack Start │             │     FastAPI     │
          │   Frontend :3000│             │    Backend :8000│
          └─────────────────┘             └────────┬────────┘
                                                   │
                                    ┌──────────────┴──────────────┐
                                    │                             │
                                    ▼                             ▼
                           ┌─────────────────┐          ┌─────────────────┐
                           │ Amazon RDS       │          │   Amazon S3     │
                           │   PostgreSQL     │          │ Resume Storage  │
                           └─────────────────┘          └─────────────────┘
```

The application is deployed on **AWS EC2**. Nginx acts as the public entry point and routes frontend and API traffic to their respective services.

---

## Tech Stack

### Frontend

* React
* TypeScript
* TanStack Start
* TanStack Router
* Vite
* Tailwind CSS
* React Query
* React Hook Form

### Backend

* Python
* FastAPI
* Uvicorn
* PostgreSQL
* AI/LLM API integration

### AWS

| Service            | Purpose                    |
| ------------------ | -------------------------- |
| **EC2**            | Application hosting        |
| **RDS PostgreSQL** | Persistent relational data |
| **S3**             | Resume/object storage      |
| **IAM**            | AWS access control         |
| **Elastic IP**     | Stable public endpoint     |

### Infrastructure

* Nginx
* systemd
* Linux
* Node.js

---

## Application Flow

```text
1. User uploads a resume
          ↓
2. Frontend sends the request to FastAPI
          ↓
3. Backend processes the resume and job description
          ↓
4. Resume/object data is stored in S3
          ↓
5. Application data is persisted in PostgreSQL
          ↓
6. AI analysis evaluates the resume against the role
          ↓
7. Structured match results are returned
          ↓
8. Results are displayed in the frontend
```

---

## Key Features

### Resume Analysis

Upload a resume and use it as the candidate profile for analysis.

### Job Matching

Compare the candidate's resume against a specific job description rather than relying on a generic resume score.

### Skill Matching

Identify skills present in the resume and compare them with the requirements of the target position.

### Missing Skills

Highlight relevant skills or requirements that are not sufficiently represented in the resume.

### AI Recommendations

Generate actionable recommendations based on the detected gaps between the resume and job description.

### Cloud Storage

Uploaded resume files are stored using Amazon S3 rather than relying solely on local instance storage.

### Persistent Database

Application data is stored in PostgreSQL running on Amazon RDS.

---

## Deployment

The application is deployed on an AWS EC2 instance.

The production environment consists of two persistent application services:

```text
Nginx
 ├── → TanStack Start / Node frontend
 └── → FastAPI / Uvicorn backend
```

Both services are managed through `systemd`, allowing them to automatically restart and start again after an EC2 reboot.

Nginx exposes port `80` publicly while the frontend and backend application processes communicate through internal ports.

---

## Project Structure

```text
skillmatch-ai/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── vite.config.ts
│   └── package.json
│
├── backend/
│   ├── app/
│   ├── ...
│   └── requirements.txt
│
├── README.md
├── .gitignore
└── .env.example
```

> Directory names may vary between frontend and backend repositories.

---

## Running Locally

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend development server will start using the project's configured development port.

### Backend

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

> The exact backend entry point should match the existing FastAPI project structure.

---

## Environment Variables

Create environment variables locally rather than committing credentials to the repository.

Example:

```env
VITE_API_URL=http://127.0.0.1:8000
```

AWS credentials, database credentials, API keys, and other secrets should **never** be committed to Git.

For AWS deployments, prefer IAM roles and environment configuration over hard-coded credentials.

---

## Security

The project follows a basic separation between the public application endpoint and internal application services.

* Port `80` is used as the public HTTP entry point.
* Frontend and backend services run on the EC2 instance.
* Database services are not intended to be publicly exposed.
* Resume files are stored in Amazon S3.
* AWS access is controlled through IAM.
* Secrets are kept outside the source repository.

---

## Future Improvements

Potential improvements include:

* HTTPS and custom domain
* User authentication
* Resume version management
* Job application tracking
* More detailed skill-gap analysis
* Resume optimization suggestions
* Job recommendation capabilities
* Analytics and historical match tracking

---

## Screenshots

### Resume Analysis

<img width="1895" height="770" alt="image" src="https://github.com/user-attachments/assets/e16c20fb-fe9c-4827-a4f4-ce0613d03e0a" />


### Job Matching Results

<img width="1896" height="876" alt="image" src="https://github.com/user-attachments/assets/e2d4c3df-e5cb-4217-9c71-3063980f7a10" />


### Dashboard

<img width="1901" height="848" alt="image" src="https://github.com/user-attachments/assets/59b152af-33b5-4c12-a78e-f97f4d1091a6" />


---

## Project Status

**Deployed and operational.**

The current version is publicly accessible through the AWS EC2 deployment:

**[http://15.252.174.56](http://15.252.174.56)**

---

## License

This project is intended for educational and portfolio purposes.
