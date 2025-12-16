# Deployment Guide

This guide explains how to deploy the **Financial Intelligence System** to the cloud so it can be accessed permanently by recruiters and users.

## Option 1: Streamlit Community Cloud (Recommended & Free)
This is the easiest way to host the dashboard.

1.  **Push your code to GitHub**:
    *   Create a new repository on GitHub.
    *   Run the following commands in your terminal:
        ```bash
        git init
        git add .
        git commit -m "Initial commit"
        git branch -M main
        git remote add origin https://github.com/YOUR_USERNAME/financial-intelligence-system.git
        git push -u origin main
        ```

2.  **Deploy on Streamlit Cloud**:
    *   Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign up/login with GitHub.
    *   Click "New app".
    *   Select your repository, branch (`main`), and main file path: `app.py`.
    *   Click **Deploy**.

The app will be live in minutes at a URL like `https://financial-intelligence-system.streamlit.app`.

## Option 2: Render (Docker Deployment)
If you want to demonstrate containerization skills.

1.  **Create a Render Account**: Go to [render.com](https://render.com).
2.  **New Web Service**:
    *   Connect your GitHub repository.
    *   Select "Docker" as the Runtime.
    *   Render will automatically find the `Dockerfile` and build it.
    *   Click **Create Web Service**.

## Option 3: Local Docker Run
To run the container locally:

```bash
docker build -t fin-system .
docker run -p 8501:8501 fin-system
```
Access at `http://localhost:8501`.

## Files for Deployment
*   `Dockerfile`: Contains instructions to build the container.
*   `requirements.txt`: Lists all Python dependencies.
