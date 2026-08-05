# VRIP Deployment Guide — Render (Backend) + Vercel (Frontend)

---

## Prerequisites

| What | Where to get it |
|---|---|
| GitHub repo pushed | `https://github.com/Kaustubh-Thallam/VRIP.git` |
| Render account (free) | https://render.com |
| Vercel account (free) | https://vercel.com |

---

## Part 1: Deploy Backend on Render

### Step 1 — Create a PostgreSQL Database

1. Go to https://dashboard.render.com → **New** → **PostgreSQL**
2. Fill in:
   - **Name**: `vrip-db`
   - **Database**: `vendor_db`
   - **User**: `vrip_user`
   - **Region**: Singapore (or closest to you)
   - **Plan**: Free
3. Click **Create Database**
4. Wait for it to become **Available** (1-2 minutes)
5. Copy the **Internal Database URL** — it looks like:
   ```
   postgresql://vrip_user:xxxxxxxx@dpg-xxxxx/vendor_db
   ```

### Step 2 — Create the Backend Web Service

1. Go to https://dashboard.render.com → **New** → **Web Service**
2. Connect your GitHub account and select the `Kaustubh-Thallam/VRIP` repository
3. Fill in these settings:

   | Setting | Value |
   |---|---|
   | **Name** | `vrip-backend` |
   | **Region** | Singapore (same as DB) |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Runtime** | Python |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | Free |

4. Scroll down to **Environment Variables** and add:

   | Key | Value |
   |---|---|
   | `DATABASE_URL` | *(paste the Internal Database URL from Step 1)* |
   | `SECRET_KEY` | *(any long random string, e.g. `openssl rand -hex 32`)* |
   | `CORS_ORIGINS` | `https://your-vercel-app.vercel.app` *(fill after Vercel deploy, see Step 6)* |
   | `FRONTEND_BASE_URL` | `https://your-vercel-app.vercel.app` *(same as above)* |
   | `SEED_ON_STARTUP` | `true` |

5. Click **Create Web Service**
6. Wait for the deploy to complete (3-5 minutes). The logs should show:
   ```
   Application startup complete.
   ```

### Step 3 — Verify Backend is Running

Open your Render service URL in a browser:
```
https://vrip-backend.onrender.com/
```
You should see:
```json
{"status": "ok", "message": "Vendor Reliability Platform API is running"}
```

Also check Swagger docs at:
```
https://vrip-backend.onrender.com/docs
```

### Step 4 — Disable Seeding After First Deploy

After the first successful deploy, go to Render Dashboard → your service → **Environment** → change `SEED_ON_STARTUP` to `false`. This prevents re-seeding the demo data on every restart.

---

## Part 2: Deploy Frontend on Vercel

### Step 5 — Import Project on Vercel

1. Go to https://vercel.com → **Add New** → **Project**
2. Connect your GitHub account and select `Kaustubh-Thallam/VRIP`
3. Fill in these settings:

   | Setting | Value |
   |---|---|
   | **Framework Preset** | Other |
   | **Root Directory** | `frontend` *(click Edit and type `frontend`)* |
   | **Build Command** | `npm run build` |
   | **Output Directory** | `dist/vendor-reliability-frontend/browser` |
   | **Install Command** | `npm install` |

4. **Node.js Version**: Go to **Settings** → **General** → set to `20.x`
5. Click **Deploy**
6. Wait for the build to complete (2-3 minutes)

### Step 6 — Set Your Render URL via .env

After Render deploy is done, you need to point the frontend to your backend.

1. Copy the `.env.example` to `.env`:
   ```bash
   cd frontend
   copy .env.example .env
   ```
2. Open `frontend/.env` and replace the placeholder:
   ```ini
   RENDER_BACKEND_URL=https://vrip.onrender.com
   ```
3. Generate the `vercel.json`:
   ```bash
   node generate-vercel-config.js
   ```
4. Commit and push:
   ```bash
   git add vercel.json
   git commit -m "Set production backend URL in vercel.json"
   git push https://github.com/Kaustubh-Thallam/VRIP.git harsha-integration-testing:main
   ```
5. Vercel will auto-redeploy

### Step 7 — Update Render CORS with Vercel URL

Go back to Render Dashboard → your backend service → **Environment** → update:

| Key | Value |
|---|---|
| `CORS_ORIGINS` | `https://vrip.vercel.app` *(your actual Vercel URL)* |
| `FRONTEND_BASE_URL` | `https://vrip.vercel.app` |

Click **Save Changes** — Render will auto-redeploy.

---

## Part 3: Verify Everything Works

### Checklist

- [ ] Open your Vercel URL (e.g. `https://vrip.vercel.app`)
- [ ] Login page loads
- [ ] Login with `admin@vendor.com` / `Admin@123`
- [ ] Dashboard shows data (not empty)
- [ ] Navigate to Vendors → list populates
- [ ] Try exporting a report (PDF/Excel)

---

## Quick Reference

| What | URL |
|---|---|
| **Frontend (Vercel)** | `https://your-app.vercel.app` |
| **Backend (Render)** | `https://vrip.onrender.com` |
| **API Docs** | `https://vrip.onrender.com/docs` |
| **GitHub Repo** | `https://github.com/Kaustubh-Thallam/VRIP` |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Frontend loads but all data is empty | `vercel.json` rewrites are still pointing to `YOUR_RENDER_BACKEND_URL`. Replace with your actual Render URL. |
| CORS errors in browser console | Update `CORS_ORIGINS` in Render env to match your exact Vercel URL (no trailing slash). |
| Backend crashes on startup | Check Render logs. Most likely `DATABASE_URL` is wrong or the PostgreSQL DB hasn't been created yet. |
| `502 Bad Gateway` on Render | Free tier spins down after 15 min of inactivity. First request after idle takes 30-60 seconds to cold-start. Just wait. |
| Login returns "invalid credentials" | Database wasn't seeded. Set `SEED_ON_STARTUP=true` in Render env and redeploy. |
| Build fails on Vercel with budget error | Already fixed — budgets are set to 2MB/5MB. If still failing, check Vercel build logs. |
| Password reset link goes to localhost | Update `FRONTEND_BASE_URL` in Render env to your Vercel URL. |

---

## Free Tier Limitations

### Render (Free)
- Backend **sleeps after 15 minutes** of inactivity → first request takes ~30-60s
- PostgreSQL free DB expires after **90 days** (you'll get email reminders to recreate)
- 750 hours/month of running time

### Vercel (Free/Hobby)
- Unlimited static deploys
- Rewrites count as serverless function invocations (100K/month free)
- Custom domains supported on free tier

---

## Want a Custom Domain?

### Vercel
1. Dashboard → Project → **Settings** → **Domains**
2. Add your domain (e.g. `vrip.yourdomain.com`)
3. Update DNS as instructed

### Render
1. Dashboard → Service → **Settings** → **Custom Domains**
2. Add your domain
3. Update `CORS_ORIGINS` to include the new frontend domain
