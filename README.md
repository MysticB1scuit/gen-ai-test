# Generative AI Media App

This project allows users to generate AI images or retrieve relevant videos using natural language prompts. It features a Flask backend powered by a pretrained Stable Diffusion model and a mobile frontend built with React Native + Expo.

The video component is based on a keyword-matching system that links prompts to a set of hand-picked videos. Earlier experimentation involved using TF-IDF to match prompts via CSV data, and using a pretrained video generation model called ModelScope. While these approaches yielded some results, they were ultimately abandoned due to high resource demands and inconsistent output. The final version focuses on a simpler and more reliable strategy that works consistently across devices.

---

## Features

- **Text-to-Image Generation** using a pretrained Stable Diffusion model
- **Text-to-Video Retrieval** using prompt keyword-matching
- **Mobile App Interface** built with React Native and Expo
- **Live API** served with Flask
- **Cloud Deployment** via AWS ECS, S3, and ECR
- **Monitoring & Observability** using CloudWatch and X-Ray

---

## Tech Stack

- **Frontend:** React Native (Expo)
- **Backend:** Flask (Python)
- **Model:** Stable Diffusion (Hugging Face)
- **Deployment:** AWS ECS (Fargate), ECR, S3
- **Infrastructure as Code:** Terraform
- **Observability:** Amazon CloudWatch, AWS X-Ray
- **Optional:** ModelScope integration script included but not active

---

## Installation & Setup

### 1. Backend Setup (Flask)

```bash
# Inside /web_app
python -m venv venv310
# On Windows:
venv310\Scripts\activate
# On macOS/Linux:
source venv310/bin/activate

pip install -r requirements.txt
python app.py
```

Ensure `load_stable_diffusion.py` is correctly downloading or referencing the Stable Diffusion model.

---

### 2. Mobile App Setup (React Native)

```bash
# Inside /generative-ai-app
npm install
npx expo start --tunnel
```

Use the Expo Go app on your mobile phone to scan the QR code.

Remember to update the API URL in `App.js`:
- Use `http://localhost:5000` when testing on your PC
- Use `http://<your-local-ip>:5000` when testing on your phone

---

## Project Structure

```
Project_Directory/
|-- generative-ai-app/      # Mobile Frontend (React Native)
|-- web_app/                # Backend (Flask + Stable Diffusion + keyword to video matching)
    |-- models/             # Model loaders (Stable Diffusion and optional ModelScope)
    |-- static/             # Output folder and sample video set
    |-- templates/          # Contains index.html (Frontend when using PC)
    |-- app.py              # Main Flask app
|-- terraform/              # Terraform IaC config for S3 + more
|-- README.md
```

---

## Cloud Deployment & Infrastructure

This project was deployed to the cloud using a fully containerized setup:

- **Amazon ECS (Fargate):** Hosts the Flask backend in a secure, scalable container service.
- **Amazon ECR:** Stores the container image built with Docker.
- **Amazon S3:** Stores all generated media files, uploaded automatically from the backend.
- **Terraform:** Used to provision AWS resources (S3 bucket, IAM roles, etc.).

### Deployment Steps

- Docker image built locally and pushed to AWS ECR.
- ECS task definitions and services created for production deployment.
- Public IP retrieved from ECS service for accessing the app externally.

---

## Observability & Monitoring

To support production-level transparency and reliability, monitoring and tracing were implemented:

### Amazon CloudWatch

- **Container Logs:** Collected from the ECS task and streamed to a log group.
- **Alarms:** CPU utilization alarm created to notify via email when thresholds are exceeded.

### AWS X-Ray

- X-Ray SDK integrated in the Flask app to trace image generation endpoints.
- Sidecar container (`xray-daemon`) added to the ECS task to relay trace data.
- Traces visualized via the X-Ray service map and timeline.

---

## Notes

- The `data/` folder was used for initial preprocessing and is excluded from GitHub.
- The CSV files (`tdiuc_questions_*.csv`) were part of an older TF-IDF based approach and are no longer used.
- The final video selection is entirely based on keyword presence in the user’s prompt.
- A script for ModelScope video generation (`load_modelscope.py`) is included for future use but not active in the current version.
- Deployment region: `eu-north-1` (Stockholm)

---

## Version Compatibility

This app was tested locally with:

- torch==2.1.0+cu121
- torchvision==0.16.0+cu121
- torchaudio==2.1.0+cu121
- diffusers==0.29.0
- modelscope==1.9.5
- aws-xray-sdk==2.14.0
- Flask==2.3.x
- Docker Desktop + WSL2
- Terraform v1.11.4

These versions ensured compatibility with GPU acceleration and pretrained models.

If you intend to use ModelScope or Stable Diffusion locally with GPU, then refer to `requirements.txt` for guidance but adjust versions as needed.

GPU acceleration was used during development but is not required in deployment.