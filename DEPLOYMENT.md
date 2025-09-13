# Deployment Guide for Render

## Prerequisites
- GitHub account
- Render account (free)

## Step 1: Push to GitHub
1. Initialize git repository: `git init`
2. Add all files: `git add .`
3. Commit: `git commit -m "Initial commit"`
4. Create GitHub repository
5. Push to GitHub: `git push origin main`

## Step 2: Deploy on Render

### Create Web Service
1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: ssdm-system (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn form_project.wsgi:application`
   - **Python Version**: 3.11

### Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `ssdm-database`
3. Click "Create Database"
4. Copy the database URL

### Configure Environment Variables
In your web service settings, add these environment variables:
- `SECRET_KEY`: Generate a secure secret key
- `DATABASE_URL`: Paste the PostgreSQL URL from step above
- `EMAIL_HOST`: Your SMTP host (e.g., smtp.gmail.com)
- `EMAIL_PORT`: 587
- `EMAIL_HOST_USER`: Your email
- `EMAIL_HOST_PASSWORD`: Your email password
- `DEFAULT_FROM_EMAIL`: noreply@yourdomain.com

## Step 3: Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

## Step 4: Create Admin Users
1. Go to your deployed app
2. Add `/admin/` to the URL
3. Create superuser or use management command

## Troubleshooting
- Check build logs if deployment fails
- Ensure all environment variables are set
- Verify database connection
- Check static files are being served correctly
