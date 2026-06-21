# Service Marketplace - Frontend (Next.js + Redux Toolkit)

## Tech Stack
- Next.js 14 (App Router) + TypeScript
- Redux Toolkit + React Redux (State Management)
- Tailwind CSS
- Axios (Backend API Calls)
- JWT Token stored in Cookies, Route Protection via Middleware

## Connection with Backend
This Frontend works connected with the `backend/` (FastAPI) project. The Backend must be started first.

## Local Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Set Environment Variables
```bash
cp .env.local.example .env.local
```
Check that the Backend API URL is correct in `.env.local`:

NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

### 3. Start the Development Server
```bash
npm run dev
```

Frontend will run at: `http://localhost:3000`

## Folder Structure (Summary)
- `src/app/` — Next.js App Router Pages (Auth/User/Vendor/Admin separated using Route Groups)
- `src/components/` — UI, Layout, Auth, Marketplace, Checkout, Vendor, Admin Components
- `src/store/` — Redux Toolkit Store and Slices (auth, service, order, vendor, admin)
- `src/lib/api/` — Separate API functions for each Backend endpoint
- `src/middleware.ts` — Role-Based Route Protection (runs at the Edge)

## How Authentication & RBAC Works
1. After Login, a JWT Token is received from the Backend and stored in Cookies (`access_token`, `user_role`)
2. An Axios Interceptor attaches the Token to the Authorization Header on every request
3. `middleware.ts` checks the Cookie before entering any Protected Route — redirects to `/unauthorized` if the Role doesn't match
4. On the Client-Side, the `ProtectedRoute` Component performs a Double-Check (stays protected even if Middleware is bypassed)
5. On receiving a 401 Response, the Axios Interceptor automatically logs the user out and redirects to the Login Page

## Test Login (Using Backend Seed Data)
| Role   | Email                  | Password   |
|--------|------------------------|------------|
| Admin  | admin@marketplace.com  | Admin123!  |
| Vendor | vendor@marketplace.com | Vendor123! |
| User   | user@marketplace.com   | User123!   |

## Production Build (Vercel Deploy)
```bash
npm run build
npm run start
```
When deploying on Vercel, the `NEXT_PUBLIC_API_URL` Environment Variable must be set (the Public URL of the Backend running on the VPS).
