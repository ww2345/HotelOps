# HotelOps (Hotel Management Demo)

A simple hotel management web app built with **Node.js + Express + EJS + MongoDB (Mongoose)**.

It includes:
- A public home page with demo hotel info + generated images.
- Admin login (MongoDB-backed) and a protected admin dashboard.
- Demo **Rooms** and **Bookings** stored in MongoDB and shown on the admin page.

## Tech stack
- **Express** (server + routing)
- **EJS + ejs-mate** (views/layouts)
- **MongoDB + Mongoose** (data)
- **express-session** (admin session)
- **Bootstrap + Font Awesome** (UI)

## Requirements
- Node.js (LTS recommended)
- MongoDB running locally

Default MongoDB connection used in `app.js`:
`mongodb://127.0.0.1:27017/hotel_management`

## Install & run
```bash
npm install
node app.js
```

Open:
- Home: `http://127.0.0.1:9999/`
- Admin login: `http://127.0.0.1:9999/login`
- Admin dashboard: `http://127.0.0.1:9999/admin`

## Routes
- `GET /` — home page
- `GET /assets/hotel-image.svg` — generated placeholder “hotel image” used on the home page
- `GET /contact` — contact page
- `GET /login` — admin login form
- `POST /login` — validates credentials (MongoDB)
- `GET /admin` — protected admin dashboard (requires login session)
- `GET /logout` — clears session and returns to `/login`

## Admin login (MongoDB)
Admin credentials are checked in MongoDB using the model in `models/AdminUsers.js`.

By default in this project, that model is bound to the **`users`** collection.

Create an admin user record (example) in the `hotel_management` DB:
```js
// Collection: users
{ "username": "admin", "password": "admin123" }
```

Then log in at `/login`.

Security note: passwords are currently compared as **plain text** (demo-only). For real apps, use hashing (bcrypt) + proper auth flows.

## Demo data seeding (Rooms & Bookings)
On successful MongoDB connection, the app seeds demo data **once** if the collections are empty:
- `rooms` (via `models/Room.js`)
- `bookings` (via `models/Booking.js`)

This makes the admin dashboard show persistent data from the database (not regenerated on each request).

## Project structure
- `app.js` — Express app, routes, auth middleware, seeding
- `models/` — Mongoose models (`AdminUsers.js`, `Room.js`, `Booking.js`)
- `views/` — EJS templates and layout
- `public/` — static assets (CSS)
