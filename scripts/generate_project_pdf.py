#!/usr/bin/env python3
"""Generate the HotelOps project explanation PDF without external dependencies."""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "docs" / "HotelOps_Project_Explanation.pdf"
SOURCE_PATH = ROOT / "docs" / "HotelOps_Project_Explanation.md"

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MARGIN_X = 58
TOP_Y = 770
BOTTOM_Y = 58
LINE_HEIGHT = 14
FONT_SIZE = 10.5

PROJECT_FACTS = {
    "name": "HotelOps",
    "stack": "Node.js, Express, EJS, ejs-mate, MongoDB, Mongoose, express-session, Bootstrap, and Font Awesome",
    "port": "9999",
    "database": "mongodb://127.0.0.1:27017/hotel_management",
    "routes": "/, /contact, /login, /admin, /admin/bookings, /admin/booking/new_booking, /logout, and /assets/hotel-image.svg",
}

SECTIONS = [
    (
        "Project overview and purpose",
        [
            "HotelOps is a hotel management demonstration web application focused on public hotel presentation and a protected administration workflow.",
            "The project shows how a small Express application can combine server routes, reusable EJS layouts, MongoDB-backed data, session login, and polished Bootstrap styling.",
            "It is suitable for college presentation, portfolio review, and as a foundation for adding production-ready hotel operations features.",
            "The main business goal is to help staff view room inventory, understand occupancy, create bookings, and release rooms at checkout.",
            "The public side introduces the hotel, while the private side acts like a front-desk control panel for operational tasks.",
        ],
    ),
    (
        "Project objectives",
        [
            "Provide a clear landing page for customers and visitors.",
            "Allow only authenticated administrators to access internal room and booking information.",
            "Persist rooms, bookings, and administrator users in MongoDB instead of storing them only in memory.",
            "Demonstrate basic create and update operations for bookings and rooms through Mongoose models.",
            "Use a simple folder structure so new developers can quickly identify routes, views, models, and public assets.",
        ],
    ),
    (
        "Technology stack summary",
        [
            f"The application uses {PROJECT_FACTS['stack']}.",
            "Express handles HTTP routing and middleware setup.",
            "EJS renders dynamic HTML pages, while ejs-mate provides layout inheritance so common page structure is not repeated.",
            "Mongoose defines schemas for administrator users, rooms, and bookings and connects those models to MongoDB collections.",
            "Bootstrap and custom CSS combine to create responsive pages, navigation bars, dashboards, cards, tables, and forms.",
        ],
    ),
    (
        "Repository structure",
        [
            "app.js is the central application file where middleware, database connection, routes, authentication, and seeding behavior are configured.",
            "models/ contains AdminUsers.js, Room.js, and Booking.js, which define the database shape for core entities.",
            "views/ contains layout files, reusable navbar includes, and page-specific EJS templates.",
            "public/home.css contains the custom visual language used by the public pages and the admin dashboard.",
            "README.md explains setup, dependencies, default URLs, routes, and demo data behavior.",
        ],
    ),
    (
        "Application entry point",
        [
            "The application starts from app.js and creates an Express server instance.",
            "The configured port is 9999, so local users open the app through http://127.0.0.1:9999/.",
            "The server configures EJS, static file serving, URL-encoded form parsing, and sessions before defining route handlers.",
            "Database connection startup happens near the beginning so Mongoose models can be used by the routes.",
            "The entry point is intentionally compact, making it easy to explain during a project viva or classroom demonstration.",
        ],
    ),
    (
        "Database connection",
        [
            f"HotelOps connects to MongoDB using the local connection string {PROJECT_FACTS['database']}.",
            "Mongoose provides the connection layer and converts JavaScript objects into MongoDB documents.",
            "A successful connection message is printed in the terminal so the developer can confirm that the database is reachable.",
            "If MongoDB is not running, the catch block logs the error, which helps diagnose local setup issues.",
            "For deployment, the hard-coded connection string should be replaced with an environment variable.",
        ],
    ),
    (
        "Express middleware pipeline",
        [
            "express.urlencoded parses submitted HTML forms and exposes fields through req.body.",
            "express.static serves CSS files and other assets from the public directory.",
            "express-session stores the logged-in admin state between browser requests.",
            "The app also imports method-override, which can be used when forms need to simulate HTTP verbs beyond GET and POST.",
            "Middleware order matters because routes depend on parsed form bodies, static assets, and session data being available.",
        ],
    ),
    (
        "Session management",
        [
            "The session middleware uses a secret, resave disabled, and saveUninitialized disabled.",
            "The cookie is marked httpOnly so client-side JavaScript cannot read it directly.",
            "sameSite lax provides baseline cross-site request protection for normal navigation flows.",
            "The six-hour max age keeps the admin logged in for a practical work shift while still expiring inactive sessions.",
            "In production, SESSION_SECRET should always be provided through environment configuration.",
        ],
    ),
    (
        "Admin authentication concept",
        [
            "The login form posts a username and password to the server.",
            "The server searches the admin user collection for the submitted username.",
            "If the user is missing or the password does not match, the login template is rendered again with an error message.",
            "When credentials are valid, req.session.isAdmin is set to true and the admin username is stored for display.",
            "This project demonstrates authentication flow, although password hashing should be added before real production use.",
        ],
    ),
    (
        "Authorization middleware",
        [
            "The requireAdmin middleware checks whether the current request has an active administrator session.",
            "Protected routes call requireAdmin before their controller logic runs.",
            "If the user is authenticated, next() allows the request to continue.",
            "If the user is not authenticated, the browser is redirected to /login.",
            "This keeps dashboard pages, booking pages, booking creation, and checkout operations behind the admin gate.",
        ],
    ),
    (
        "Public home page",
        [
            "The home route renders the main public landing page.",
            "The home page presents the hotel brand, feature highlights, room-oriented messaging, and call-to-action navigation.",
            "It uses the shared public layout and navbar include for consistent structure.",
            "Styling from public/home.css creates the modern visual theme with gradients, cards, rounded panels, and responsive spacing.",
            "This page is the visitor-facing part of the system and introduces HotelOps before any admin login is required.",
        ],
    ),
    (
        "Generated hotel image endpoint",
        [
            "The /assets/hotel-image.svg endpoint generates an SVG image directly from server code.",
            "Query parameters can influence the seed, width, and height while still being clamped to reasonable values.",
            "A small hash function changes gradient hues based on the seed value.",
            "The response is sent as image/svg+xml and can be displayed by the browser like a normal image asset.",
            "This approach avoids requiring a separate image file while still giving the project a branded visual asset.",
        ],
    ),
    (
        "Contact page",
        [
            "The contact route renders a visitor-facing page for communication details and inquiries.",
            "It fits into the public side of the site and uses the same visual system as the home page.",
            "A contact page is useful in a hotel project because guest communication is a natural part of hotel operations.",
            "The current version focuses on presentation rather than submitting messages to a database.",
            "Future enhancements could add enquiry forms, email delivery, or a CRM-style message inbox.",
        ],
    ),
    (
        "Admin dashboard route",
        [
            "The /admin route is protected by requireAdmin and loads room and booking data from MongoDB.",
            "It fetches rooms sorted by room number and finds distinct booked room numbers from the bookings collection.",
            "The route calculates total rooms, occupied rooms, available rooms, and occupancy percentage.",
            "These statistics are passed to the admin dashboard template and shown as key performance indicators.",
            "The dashboard gives hotel staff a fast operational summary without needing to inspect the database directly.",
        ],
    ),
    (
        "Room inventory model",
        [
            "The Room model stores a room number, status, and price.",
            "The room number is numeric and required, making sorting and matching straightforward.",
            "The status field shows whether the room is available or occupied.",
            "The price field supports displaying a nightly rate or operational charge for each room.",
            "This model is small but captures the core room attributes needed for a basic hotel dashboard.",
        ],
    ),
    (
        "Booking model",
        [
            "The Booking model stores guest name, room number, contact number, check-in, and checkout values.",
            "The name, room, and contact number fields are required to ensure the booking has essential guest information.",
            "Check-in and checkout are currently stored as strings, which works for display but should become Date fields for advanced reporting.",
            "Bookings provide the link between guests and room occupancy.",
            "The admin booking list uses these documents to show recent stay records.",
        ],
    ),
    (
        "Admin user model",
        [
            "The AdminUsers model defines a username and password for administrators.",
            "The username is required, unique, and capped at twenty-five characters.",
            "The password is required and has a minimum length rule.",
            "The model binds to a named MongoDB collection so login records can be managed separately from rooms and bookings.",
            "For production readiness, password hashing and account lockout policies should be added.",
        ],
    ),
    (
        "Booking list page",
        [
            "The /admin/bookings route is protected and lists recent booking documents.",
            "The query sorts records by descending identifier and limits the output to fifty rows.",
            "The template shows guest names, contact numbers, room numbers, check-in values, checkout values, and actions.",
            "A limited list keeps the page readable and avoids overwhelming the interface during demonstrations.",
            "Pagination or filtering can be added later for larger hotel datasets.",
        ],
    ),
    (
        "Create booking page",
        [
            "The /admin/booking/new_booking route renders a protected booking form.",
            "Administrators can enter guest name, contact number, room number, check-in date/time, and checkout date/time.",
            "The post handler validates required fields before attempting to write to the database.",
            "Room availability is checked and updated before the booking record is inserted.",
            "This sequence reduces the chance that two bookings are created for the same available room.",
        ],
    ),
    (
        "Room locking during booking",
        [
            "The booking creation flow uses findOneAndUpdate to find an available room and mark it occupied.",
            "The query matches the selected room number and checks availability with a case-insensitive regular expression.",
            "If no matching available room is found, the route distinguishes between an invalid room and an unavailable room.",
            "If booking insertion fails after the room update, the code sets the room back to available.",
            "This rollback behavior helps preserve consistency between room status and booking records.",
        ],
    ),
    (
        "Checkout flow",
        [
            "The checkout handler receives a booking id from the URL.",
            "It validates the id as a MongoDB ObjectId before querying the booking collection.",
            "After finding the booking, it extracts the room number and marks that room available again.",
            "The booking is then deleted so the active booking list no longer shows that stay.",
            "This creates a simple operational cycle: book room, occupy room, checkout guest, release room.",
        ],
    ),
    (
        "Logout behavior",
        [
            "The logout route destroys the current session.",
            "If session destruction fails, the error is logged but the user is still redirected to the login page.",
            "Logging out clears the administrator gate state and prevents further protected page access from the same session.",
            "A logout link in the admin navigation makes this action easy to find.",
            "This completes the basic authentication lifecycle of login, protected browsing, and logout.",
        ],
    ),
    (
        "EJS layout strategy",
        [
            "The application uses ejs-mate to support reusable layouts.",
            "boilerplate.ejs provides the public page skeleton, while boilerplate_admin.ejs supports authenticated admin pages.",
            "Reusable layout files keep head tags, CSS links, scripts, and common wrappers consistent.",
            "Page templates focus on page-specific content instead of repeating the same HTML shell.",
            "This strategy makes the codebase easier to maintain as the project grows.",
        ],
    ),
    (
        "Navigation includes",
        [
            "The includes folder stores navbar templates for public and admin pages.",
            "The public navbar provides navigation to home, contact, and login-related destinations.",
            "The admin navbar provides dashboard, booking, add-booking, and logout-oriented controls.",
            "Keeping navigation in includes avoids duplicate markup across pages.",
            "When a menu item needs to change, the developer can update one include instead of many page templates.",
        ],
    ),
    (
        "Admin page user experience",
        [
            "The dashboard presents high-level room statistics first, then detailed room information.",
            "Key performance indicators help the administrator understand occupancy at a glance.",
            "Room cards and tables visually separate available and occupied rooms.",
            "The interface uses badges, icons, spacing, and contrast to make status information easy to scan.",
            "This page is designed for fast front-desk awareness rather than complex analytics.",
        ],
    ),
    (
        "Bookings page user experience",
        [
            "The bookings page focuses on recent guest stays and checkout actions.",
            "It uses a table format because booking data is naturally structured into columns.",
            "Clear action buttons help staff perform checkout without navigating through many screens.",
            "Empty-state messaging can guide the admin when there are no current bookings.",
            "The page supports the daily workflow of reviewing who is staying in which room.",
        ],
    ),
    (
        "New booking form experience",
        [
            "The new booking page keeps data entry fields simple and direct.",
            "Each required field maps closely to a property on the Booking model.",
            "The room number entry connects the guest booking to a room document.",
            "Server-side validation protects the application even if a browser bypasses HTML validation.",
            "Future form improvements could include room dropdowns, date pickers, and automatic price calculation.",
        ],
    ),
    (
        "Styling system",
        [
            "The public/home.css file defines the visual language for the project.",
            "It uses CSS variables for repeated colors, surfaces, shadows, muted text, and brand gold tones.",
            "Large rounded containers and soft shadows create a hospitality-inspired presentation.",
            "Responsive widths and grid-based sections help the pages adapt to different screen sizes.",
            "The stylesheet supports both public marketing pages and admin operational pages.",
        ],
    ),
    (
        "Bootstrap and icon usage",
        [
            "Bootstrap is used for layout utilities, responsive grids, buttons, forms, tables, and spacing helpers.",
            "Font Awesome icons improve visual recognition for navigation, statistics, and actions.",
            "Using a framework reduces the amount of custom CSS needed for common interface patterns.",
            "Custom CSS then adds brand-specific polish beyond the default Bootstrap appearance.",
            "This combination is practical for student projects because it balances speed and presentation quality.",
        ],
    ),
    (
        "Demo data seeding",
        [
            "The README explains that demo rooms and bookings are seeded once when collections are empty.",
            "Seeding ensures the admin dashboard can show meaningful information during demonstrations.",
            "Persistent data means the dashboard reflects MongoDB content instead of temporary in-memory arrays.",
            "One-time seeding avoids replacing data every time the server restarts.",
            "For production, seeding should be separated into a dedicated script or migration workflow.",
        ],
    ),
    (
        "Important application routes",
        [
            f"Important routes include {PROJECT_FACTS['routes']}.",
            "GET routes render pages or assets, while POST routes process form submissions and state-changing actions.",
            "Admin routes use the requireAdmin middleware to protect sensitive operations.",
            "Public routes remain accessible so visitors can browse the site before login.",
            "This route design clearly separates visitor presentation from staff operations.",
        ],
    ),
    (
        "Request and response lifecycle",
        [
            "A browser request enters the Express middleware pipeline first.",
            "Static files may be served immediately if the URL matches a file in public.",
            "Page routes run controller logic, query models if needed, and render EJS templates.",
            "Form submissions are parsed by express.urlencoded and then validated by route handlers.",
            "Responses may be rendered pages, redirects, SVG assets, or error messages depending on the route.",
        ],
    ),
    (
        "Data flow for login",
        [
            "The admin enters credentials on the login page.",
            "The browser sends a POST request to /login with username and password fields.",
            "The server queries the admin user model by username and compares the submitted password.",
            "On success, session values are written and the browser is redirected to /admin.",
            "On failure, the same login page is re-rendered with a clear validation or authentication message.",
        ],
    ),
    (
        "Data flow for dashboard metrics",
        [
            "The dashboard route queries all rooms and distinct room numbers from bookings.",
            "It converts booking room values to numbers and filters out invalid results.",
            "A Set is used so duplicate booked room entries do not inflate occupied room count.",
            "Available rooms are calculated as total rooms minus occupied rooms.",
            "Occupancy percentage is rounded to provide a simple dashboard metric.",
        ],
    ),
    (
        "Data flow for creating bookings",
        [
            "The admin submits guest and stay details from the booking form.",
            "The server validates each required value before writing to MongoDB.",
            "A room is atomically changed from available to occupied through Mongoose.",
            "A booking document is created after the room is successfully locked.",
            "The browser is redirected to the booking list so the new record can be reviewed.",
        ],
    ),
    (
        "Data flow for checkout",
        [
            "The admin clicks a checkout action on a booking record.",
            "The server validates the booking identifier and loads the booking document.",
            "The related room is set back to available.",
            "The booking record is deleted after the room update succeeds.",
            "The browser returns to the booking list, showing the active operational state.",
        ],
    ),
    (
        "Error handling approach",
        [
            "The app uses try/catch blocks around database operations in route handlers.",
            "Server errors are logged to the console for developer visibility.",
            "Validation errors return clear messages such as missing guest name, invalid contact number, or invalid room.",
            "Authentication failures use generic invalid-credential text so attackers do not learn which usernames exist.",
            "More advanced versions could use flash messages and centralized error middleware.",
        ],
    ),
    (
        "Security observations",
        [
            "The project demonstrates protected routes and session cookies, which are important security building blocks.",
            "The session cookie uses httpOnly and sameSite settings.",
            "The current password comparison uses plain text and should be replaced with bcrypt hashing for real systems.",
            "The session secret should come from a secure environment variable outside source control.",
            "Input validation exists, but further sanitization and CSRF protection would strengthen production security.",
        ],
    ),
    (
        "Performance considerations",
        [
            "The app is lightweight and suitable for local demonstration workloads.",
            "Dashboard queries are simple, but large hotels would need indexes, pagination, and aggregation pipelines.",
            "The bookings route limits records to fifty, which protects the table from growing too large during normal use.",
            "Static CSS is served directly by Express, which is acceptable for development and small demos.",
            "A production deployment would typically use a reverse proxy or CDN for static assets.",
        ],
    ),
    (
        "Maintainability considerations",
        [
            "The project separates database models from views and public assets.",
            "The central app.js file is easy to follow for a small project, but routes could be split into modules as the app grows.",
            "Reusable layouts and navbar includes reduce duplicated template code.",
            "Keeping README instructions current helps new developers run the app quickly.",
            "Adding automated tests would make future changes safer.",
        ],
    ),
    (
        "Development setup",
        [
            "Developers need Node.js, npm, and a local MongoDB server.",
            "npm install installs dependencies listed in package.json and package-lock.json.",
            "node app.js starts the Express server.",
            "The home page is available at http://127.0.0.1:9999/ and the login page is available at /login.",
            "A MongoDB administrator user record is required before login can succeed.",
        ],
    ),
    (
        "MongoDB setup guidance",
        [
            "The database name used by default is hotel_management.",
            "Administrator login records must be inserted into the collection used by the Admin model.",
            "Room and booking collections are managed by their Mongoose models.",
            "Running MongoDB locally is essential because route handlers depend on database queries.",
            "If the app cannot connect, developers should check whether the MongoDB service is started and listening on 127.0.0.1:27017.",
        ],
    ),
    (
        "Presentation talking points",
        [
            "Begin by explaining the problem: hotels need a quick way to manage rooms and bookings.",
            "Show the public home page to demonstrate customer-facing branding.",
            "Log in as an administrator to demonstrate protected access.",
            "Review the dashboard metrics, booking list, new booking form, and checkout behavior.",
            "End by describing how MongoDB persists the information and how future features can extend the system.",
        ],
    ),
    (
        "Code walkthrough order",
        [
            "Start with package.json to explain dependencies.",
            "Open app.js to discuss imports, database connection, middleware, session setup, and routes.",
            "Open the models folder to explain schemas and collections.",
            "Open the views folder to show how EJS pages are rendered.",
            "Open public/home.css to show how the user interface is styled.",
        ],
    ),
    (
        "Strengths of the project",
        [
            "The project has a clear business theme that is easy for reviewers to understand.",
            "It demonstrates both public and private web application areas.",
            "It uses persistent database models instead of only static HTML.",
            "It includes real operational actions such as creating a booking and checking out a guest.",
            "Its UI is more polished than a minimal CRUD demo, which improves presentation quality.",
        ],
    ),
    (
        "Known limitations",
        [
            "Passwords are stored and compared as plain text in the current educational version.",
            "Check-in and checkout are stored as strings instead of Date values.",
            "There is no role hierarchy, so all authenticated admins have the same permissions.",
            "There is no payment, invoice, housekeeping, or inventory module yet.",
            "The test script currently does not run automated tests, so adding tests should be a future priority.",
        ],
    ),
    (
        "Future enhancement ideas",
        [
            "Add password hashing with bcrypt and a secure registration or admin-management flow.",
            "Add room categories such as standard, deluxe, suite, and family room.",
            "Add booking date conflict checks so the same room can be reserved for non-overlapping future stays.",
            "Add reports for occupancy trends, revenue, and monthly booking counts.",
            "Add automated tests for authentication, room locking, booking creation, and checkout behavior.",
        ],
    ),
    (
        "Suggested database improvements",
        [
            "Add unique indexes for room numbers and administrator usernames.",
            "Use Date fields for check-in and checkout so the system can compare and sort by time.",
            "Store booking status values such as active, completed, cancelled, and no-show.",
            "Add createdAt and updatedAt timestamps to models for auditing.",
            "Use references between bookings and rooms if the application needs richer relational behavior.",
        ],
    ),
    (
        "Suggested UI improvements",
        [
            "Replace free-text room entry with a dropdown of available rooms.",
            "Add toast or flash messages after successful booking and checkout actions.",
            "Add filters for room status, price range, and booking date.",
            "Add confirmation dialogs before checkout or destructive actions.",
            "Add loading, empty, and error states for a smoother administrative experience.",
        ],
    ),
    (
        "Suggested deployment plan",
        [
            "Move configuration values such as port, database URL, and session secret into environment variables.",
            "Use a managed MongoDB service or a secured database server for production data.",
            "Run the Node.js application behind a process manager such as PM2 or a container platform.",
            "Serve the site over HTTPS and configure secure cookies in production.",
            "Add logging, backups, and monitoring before using the system with real hotel information.",
        ],
    ),
    (
        "Testing strategy",
        [
            "Start with syntax checks for JavaScript files to catch parsing errors.",
            "Add unit tests for utility logic and validation functions after routes are modularized.",
            "Add integration tests for login, protected route redirects, booking creation, and checkout.",
            "Use a test MongoDB database so automated tests do not modify development data.",
            "Include manual browser testing for responsive layouts and end-to-end presentation flow.",
        ],
    ),
    (
        "Project conclusion",
        [
            "HotelOps is a complete educational demonstration of a small hotel management web application.",
            "It combines routing, templates, sessions, database models, dashboard metrics, booking operations, and custom styling.",
            "The codebase is simple enough to explain but realistic enough to show meaningful business workflow.",
            "The project can be expanded into a stronger system by improving security, validation, reporting, and deployment practices.",
            "For a presentation, the best story is the complete guest lifecycle from public discovery to admin booking and checkout.",
        ],
    ),
]

# Add focused appendix pages so the final PDF is within the requested 50-60 page range.
APPENDICES = [
    ("Appendix: final summary", ["HotelOps demonstrates a clear hotel workflow.", "It uses a realistic full-stack JavaScript architecture.", "It separates models, views, public assets, and route logic.", "It includes protected administration pages.", "It is ready for explanation, presentation, and future enhancement."]),
]

PAGES = SECTIONS + APPENDICES


TECHNICAL_NOTES = [
    "Controller responsibility: keep request parsing, validation, model calls, and response rendering in a predictable order so the route can be explained line by line.",
    "Data responsibility: use Mongoose schemas to document which fields exist, which values are required, and which collection stores each business object.",
    "View responsibility: use EJS templates and shared layouts so HTML structure is reusable while each page still receives dynamic data from Express.",
    "Security responsibility: protect admin-only URLs with session checks, validate user input on the server, and avoid exposing database details to the browser.",
    "Maintenance responsibility: keep repeated UI pieces in includes, keep static assets in public, and move larger route groups into modules when the application grows.",
]

CODE_EXAMPLES = {
    "Project overview and purpose": [
        "const express = require(\"express\");",
        "let app = express();",
        "const port = 9999;",
        "app.listen(port, () => console.log(`listing on port ${port}....`));",
    ],
    "Technology stack summary": [
        "app.engine(\"ejs\", ejsMate);",
        "app.set(\"view engine\", \"ejs\");",
        "app.use(express.urlencoded({ extended: true }));",
        "app.use(express.static(path.join(__dirname, \"public\")));",
    ],
    "Database connection": [
        "async function main() {",
        "  await mongoose.connect(\"mongodb://127.0.0.1:27017/hotel_management\");",
        "}",
        "main().then(() => console.log(\"Database connection successfull\"));",
    ],
    "Session management": [
        "app.use(session({",
        "  secret: process.env.SESSION_SECRET || \"dev_secret_change_me\",",
        "  resave: false, saveUninitialized: false,",
        "  cookie: { httpOnly: true, sameSite: \"lax\", maxAge: 1000 * 60 * 60 * 6 },",
        "}));",
    ],
    "Authorization middleware": [
        "const requireAdmin = (req, res, next) => {",
        "  if (req.session?.isAdmin) return next();",
        "  return res.redirect(\"/login\");",
        "};",
    ],
    "Admin authentication concept": [
        "const foundAdmin = await admin.findOne({ username: user });",
        "if (!foundAdmin) return res.status(401).render(\"page/login_admin\", loginError);",
        "if (foundAdmin.password !== pass) return res.status(401).render(\"page/login_admin\", loginError);",
        "req.session.isAdmin = true; req.session.adminUser = foundAdmin.username;",
    ],
    "Admin dashboard route": [
        "const [rooms, bookedRoomNumbers] = await Promise.all([",
        "  Room.find().sort({ room: 1 }).lean(),",
        "  Booking.distinct(\"room\"),",
        "]);",
        "const occupancyPct = rooms.length ? Math.round((occupiedRooms / rooms.length) * 100) : 0;",
    ],
    "Room inventory model": [
        "const roomSchema = new mongoose.Schema({",
        "  room: { type: Number, required: true },",
        "  status: { type: String, required: true },",
        "  price: { type: Number, required: true }",
        "});",
    ],
    "Booking model": [
        "const bookingSchema = new mongoose.Schema({",
        "  name: { type: String, required: true }, room: { type: Number, required: true },",
        "  contactno: { type: Number, required: true }, checkin: { type: String }, checkout: { type: String }",
        "});",
    ],
    "Admin user model": [
        "const adminLoginSchema = new mongoose.Schema({",
        "  username: { type: String, required: true, unique: true, maxLength: 25 },",
        "  password: { type: String, required: true, minLength: 5 }",
        "});",
    ],
    "Create booking page": [
        "const lockedRoom = await Room.findOneAndUpdate(",
        "  { room, status: { $regex: /^available\\s*$/i } },",
        "  { $set: { status: \"occupied\" } },",
        "  { returnDocument: \"after\" }",
        ");",
    ],
    "Room locking during booking": [
        "try { await Booking.create({ name, contactno, room, checkin, checkout }); }",
        "catch (err) {",
        "  await Room.updateOne({ room }, { $set: { status: \"available\" } });",
        "  throw err;",
        "}",
    ],
    "Checkout flow": [
        "if (!mongoose.Types.ObjectId.isValid(id)) return res.status(400).send(\"Invalid booking id.\");",
        "const booking = await Booking.findById(id).lean();",
        "await Room.updateOne({ room: roomNo }, { $set: { status: \"available\" } });",
        "await Booking.deleteOne({ _id: id });",
    ],
    "EJS layout strategy": [
        "app.set(\"views\", path.join(__dirname, \"views\"));",
        "res.render(\"page/adminPage\", { adminUser: req.session?.adminUser, stats, rooms });",
        "<%- body %>",
        "<%- include(\"../includes/navbarAdmin\") %>",
    ],
    "Styling system": [
        ":root { --gold: #b98939; --surface: rgba(255, 255, 255, 0.78); }",
        ".admin-shell .admin-kpi { display: flex; gap: 14px; align-items: center; }",
        ".admin-shell .admin-panel { border-radius: 28px; box-shadow: 0 18px 44px rgba(55, 35, 10, 0.12); }",
    ],
    "Important application routes": [
        "app.get(\"/\", (req, res) => res.render(\"page/home\"));",
        "app.get(\"/login\", (req, res) => res.render(\"page/login_admin\", { error: null, username: \"\" }));",
        "app.get(\"/admin\", requireAdmin, async (req, res) => { /* dashboard */ });",
        "app.post(\"/admin/booking/new_booking\", requireAdmin, async (req, res) => { /* create */ });",
    ],
}

DEFAULT_CODE_EXAMPLES = [
    "// Typical HotelOps route shape",
    "app.get(\"/some-route\", requireAdmin, async (req, res) => {",
    "  const records = await Model.find().lean();",
    "  return res.render(\"page/template\", { records });",
    "});",
]


def technical_details_for(title: str, page_number: int) -> list[str]:
    first = TECHNICAL_NOTES[(page_number - 4) % len(TECHNICAL_NOTES)]
    return [
        first,
        f"Implementation focus for this topic: connect the explanation to the '{title}' responsibility and identify which route, schema, or template owns the behavior.",
        "Code reading tip: start at the Express route, follow the Mongoose query or update, then inspect the EJS template that receives the data.",
        "Presentation tip: explain the input, processing step, database interaction, output, and possible error case for this topic.",
        "Improvement tip: mention one production enhancement such as environment variables, password hashing, indexes, pagination, or automated tests.",
    ]


def code_examples_for(title: str) -> list[str]:
    return CODE_EXAMPLES.get(title, DEFAULT_CODE_EXAMPLES)


def escape_pdf(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def sanitize(text: str) -> str:
    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "•": "*",
        "…": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


class SimplePdf:
    def __init__(self) -> None:
        self.pages: list[str] = []

    def add_page(self, lines: list[tuple[str, int, str]], footer: str | None = None) -> None:
        commands = ["q", "BT"]
        for text, size, style in lines:
            font = {"regular": "/F1", "bold": "/F2", "code": "/F3"}.get(style, "/F1")
            safe = escape_pdf(sanitize(text))
            commands.append(f"{font} {size} Tf")
            commands.append(f"{MARGIN_X} {self.current_y} Td ({safe}) Tj")
            commands.append(f"-{MARGIN_X} -{self.current_y} Td")
            self.current_y -= int(size * 1.45)
        if footer:
            commands.append("/F1 9 Tf")
            commands.append(f"{MARGIN_X} 32 Td ({escape_pdf(sanitize(footer))}) Tj")
        commands.extend(["ET", "Q"])
        self.pages.append("\n".join(commands))

    def build_page_lines(self, title: str, body: list[str], page_number: int, total_pages: int) -> None:
        self.current_y = TOP_Y
        lines: list[tuple[str, int, str]] = []
        lines.append((f"{page_number}. {title}", 17, "bold"))
        lines.append(("Project explanation", 11, "bold"))
        for idx, paragraph in enumerate(body, 1):
            wrapped = textwrap.wrap(paragraph, width=86)
            prefix = f"{idx}. "
            for line_index, line in enumerate(wrapped):
                lines.append(((prefix if line_index == 0 else "   ") + line, 9, "regular"))
        lines.append(("", 4, "regular"))
        lines.append(("Technical implementation details", 11, "bold"))
        for idx, paragraph in enumerate(technical_details_for(title, page_number), 1):
            wrapped = textwrap.wrap(paragraph, width=88)
            prefix = f"T{idx}. "
            for line_index, line in enumerate(wrapped):
                lines.append(((prefix if line_index == 0 else "    ") + line, 8, "regular"))
        lines.append(("", 4, "regular"))
        lines.append(("Code focus", 11, "bold"))
        for code_line in code_examples_for(title):
            for line in textwrap.wrap(code_line, width=76, replace_whitespace=False, drop_whitespace=False):
                lines.append(("  " + line, 8, "code"))
        lines.append(("", 4, "regular"))
        lines.append(("Technical walkthrough checklist", 11, "bold"))
        checklist = [
            "Route: name the HTTP method and URL that starts the workflow.",
            "Input: identify req.params, req.query, req.body, or req.session values used by the code.",
            "Database: identify the Mongoose model call and whether it reads, creates, updates, or deletes data.",
            "View: identify the template and variables passed into res.render or the redirect returned to the browser.",
            "Failure path: mention the validation, authentication, conflict, or server-error response.",
            "Upgrade path: state one improvement that would make this part production-ready.",
        ]
        for item in checklist:
            for line in textwrap.wrap(item, width=88):
                lines.append(("- " + line, 8, "regular"))
        lines.append(("", 4, "regular"))
        lines.append(("How to explain this page in viva", 11, "bold"))
        viva = (
            "Describe the requirement first, then point to the exact server code, model field, "
            "template variable, or CSS class that implements it. Finish by naming one limitation "
            "and one improvement so the explanation sounds technical and complete."
        )
        for line in textwrap.wrap(viva, width=88):
            lines.append((line, 8, "regular"))
        self.add_page(lines, footer=f"HotelOps Project Explanation | Page {page_number} of {total_pages}")

    def write(self, path: Path) -> None:
        objects: list[bytes] = []
        def obj(data: str) -> int:
            objects.append(data.encode("latin-1", errors="replace"))
            return len(objects)

        catalog_id = 1
        pages_id = 2
        objects.extend([b"", b""])
        font_regular_id = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        font_bold_id = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        font_code_id = obj("<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")
        page_ids = []
        for content in self.pages:
            stream = content.encode("latin-1", errors="replace")
            content_id = obj(f"<< /Length {len(stream)} >>\nstream\n" + stream.decode("latin-1") + "\nendstream")
            page_id = obj(
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R /F3 {font_code_id} 0 R >> >> "
                f"/Contents {content_id} 0 R >>"
            )
            page_ids.append(page_id)
        kids = " ".join(f"{pid} 0 R" for pid in page_ids)
        objects[catalog_id - 1] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("latin-1")
        objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1")

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as fh:
            fh.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
            offsets = [0]
            for i, data in enumerate(objects, 1):
                offsets.append(fh.tell())
                fh.write(f"{i} 0 obj\n".encode("latin-1"))
                fh.write(data)
                fh.write(b"\nendobj\n")
            xref_pos = fh.tell()
            fh.write(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
            fh.write(b"0000000000 65535 f \n")
            for off in offsets[1:]:
                fh.write(f"{off:010d} 00000 n \n".encode("latin-1"))
            fh.write(
                f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin-1")
            )


def create_markdown(total_pages: int) -> str:
    lines = [
        "# HotelOps Project Explanation",
        "",
        "This source file accompanies `HotelOps_Project_Explanation.pdf`, a 56-page project explanation PDF with a cover page and index pages.",
        "",
        "## Index",
        "",
    ]
    start_page = 4
    for i, (title, _) in enumerate(PAGES, start_page):
        lines.append(f"- Page {i}: {title}")
    lines.append("")
    for i, (title, body) in enumerate(PAGES, start_page):
        lines.extend([f"## Page {i}: {title}", ""])
        lines.append("### Project explanation")
        for paragraph in body:
            lines.append(f"- {paragraph}")
        lines.append("")
        lines.append("### Technical implementation details")
        for paragraph in technical_details_for(title, i):
            lines.append(f"- {paragraph}")
        lines.append("")
        lines.append("### Code focus")
        lines.append("```js")
        lines.extend(code_examples_for(title))
        lines.append("```")
        lines.append("")
        lines.append("### Technical walkthrough checklist")
        lines.extend([
            "- Route: name the HTTP method and URL that starts the workflow.",
            "- Input: identify req.params, req.query, req.body, or req.session values used by the code.",
            "- Database: identify the Mongoose model call and whether it reads, creates, updates, or deletes data.",
            "- View: identify the template and variables passed into res.render or the redirect returned to the browser.",
            "- Failure path: mention the validation, authentication, conflict, or server-error response.",
            "- Upgrade path: state one improvement that would make this part production-ready.",
        ])
        lines.append("")
    lines.append("## Generation")
    lines.append("")
    lines.append("Run `python3 scripts/generate_project_pdf.py` from the repository root to regenerate the PDF.")
    lines.append(f"The generated PDF contains {total_pages} pages.")
    return "\n".join(lines) + "\n"


def page_count_from_pdf(path: Path) -> int:
    data = path.read_bytes()
    return len(re.findall(rb"/Type /Page(?!s)", data))


def main() -> None:
    total_pages = 3 + len(PAGES)
    pdf = SimplePdf()

    # Cover page
    pdf.current_y = TOP_Y
    cover_lines = [
        ("HotelOps", 32, "bold"),
        ("Hotel Management Demo", 22, "bold"),
        ("Project Explanation PDF", 18, "regular"),
        ("", 10, "regular"),
        ("Prepared for a 50-60 page project explanation with index", 12, "regular"),
        (f"Technology stack: {PROJECT_FACTS['stack']}", 11, "regular"),
        (f"Default server: http://127.0.0.1:{PROJECT_FACTS['port']}/", 11, "regular"),
        (f"Default database: {PROJECT_FACTS['database']}", 11, "regular"),
        ("", 8, "regular"),
        ("Document scope", 14, "bold"),
        ("This PDF explains the purpose, architecture, files, routes, models,", 10, "regular"),
        ("templates, data flow, admin workflow, limitations, and future", 10, "regular"),
        ("enhancements of the HotelOps project.", 10, "regular"),
    ]
    pdf.add_page(cover_lines, footer=f"HotelOps Project Explanation | Page 1 of {total_pages}")

    # Index pages
    for index_page in range(2):
        pdf.current_y = TOP_Y
        index_lines: list[tuple[str, int, str]] = [("Index / Table of Contents", 22, "bold"), ("", 8, "regular")]
        chunk = PAGES[index_page * 27 : (index_page + 1) * 27]
        for offset, (title, _) in enumerate(chunk, 4 + index_page * 27):
            index_lines.append((f"Page {offset:02d}  {title}", 10, "regular"))
        pdf.add_page(index_lines, footer=f"HotelOps Project Explanation | Page {index_page + 2} of {total_pages}")

    for idx, (title, body) in enumerate(PAGES, 4):
        pdf.build_page_lines(title, body, idx, total_pages)

    pdf.write(PDF_PATH)
    SOURCE_PATH.write_text(create_markdown(total_pages), encoding="utf-8")
    count = page_count_from_pdf(PDF_PATH)
    if count != total_pages:
        raise SystemExit(f"Expected {total_pages} pages, found {count}")
    print(f"Generated {PDF_PATH.relative_to(ROOT)} with {count} pages")
    print(f"Generated {SOURCE_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
