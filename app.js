const express = require("express");
const path = require("path");
const mongoose = require("mongoose");
const methodOverride = require("method-override");
const ejsMate = require("ejs-mate");
const session = require("express-session");
const admin = require("./models/AdminUsers");
const Room = require("./models/Room");
const Booking = require("./models/Booking");

let app = express();
const port = 9999;

async function main() {
  await mongoose.connect("mongodb://127.0.0.1:27017/hotel_management");
}

main()
  .then(async () => {
    console.log("Database connection successfull");
    try {
      await seedDemoDataIfEmpty();
    } catch (err) {
      console.error("Seed error:", err);
    }
  })
  .catch((err) => {
    console.log(err);
  });

app.engine("ejs", ejsMate);
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));
app.use(
  session({
    secret: process.env.SESSION_SECRET || "dev_secret_change_me",
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      sameSite: "lax",
      maxAge: 1000 * 60 * 60 * 6,
    },
  })
);

const pick = (items) => items[Math.floor(Math.random() * items.length)];
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const randomFloat = (min, max, decimals = 1) => {
  const value = min + Math.random() * (max - min);
  return Number(value.toFixed(decimals));
};

const requireAdmin = (req, res, next) => {
  if (req.session?.isAdmin) return next();
  return res.redirect("/login");
};

const seedDemoDataIfEmpty = async () => {
  const roomCount = await Room.estimatedDocumentCount();
  const bookingCount = await Booking.estimatedDocumentCount();
  if (roomCount > 0 && bookingCount > 0) return;

  const roomTypes = ["Standard", "Deluxe", "Suite", "Family", "Executive"];
  const roomStatuses = ["Available", "Occupied", "Cleaning", "Maintenance"];
  const bookingStatuses = ["Confirmed", "Checked-in", "Checked-out", "Cancelled"];
  const paymentStatuses = ["Paid", "Pending", "Refunded"];
  const guestsFirst = ["Aarav", "Ishant", "Diya", "Anaya", "Rohan", "Meera", "Kabir", "Isha", "Arjun", "Sana"];
  const guestsLast = ["Sharma", "Dahiya", "Verma", "Gupta", "Singh", "Patel", "Khan", "Jain", "Nair", "Iyer"];

  const today = new Date();
  const yyyymmdd = `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, "0")}${String(
    today.getDate()
  ).padStart(2, "0")}`;

  const makeDate = (offsetDays) => {
    const d = new Date(today);
    d.setHours(12, 0, 0, 0);
    d.setDate(d.getDate() + offsetDays);
    return d;
  };

  if (roomCount === 0) {
    const rooms = Array.from({ length: 30 }, (_, i) => {
      const floor = 1 + Math.floor(i / 10);
      const number = floor * 100 + (i % 10) + 1;
      const status = pick(roomStatuses);
      const housekeeping = status === "Cleaning" ? "In progress" : pick(["Ready", "Pending", "In progress"]);
      const type = pick(roomTypes);
      const rate = randomInt(2200, 9500);
      return { number, floor, type, status, housekeeping, rate };
    });
    await Room.insertMany(rooms, { ordered: false });
  }

  if (bookingCount === 0) {
    const rooms = await Room.find({}, { number: 1 }).lean();
    const roomNumbers = rooms.map((r) => r.number);
    const bookings = Array.from({ length: 22 }, (_, i) => {
      const nights = randomInt(1, 5);
      const checkInOffset = randomInt(-2, 4);
      const status = pick(bookingStatuses);
      const paymentStatus = pick(paymentStatuses);
      const guest = `${pick(guestsFirst)} ${pick(guestsLast)}`;
      const room = pick(roomNumbers);
      const amount = randomInt(2800, 24000);
      return {
        bookingId: `BK-${yyyymmdd}-${100 + i}`,
        guest,
        room,
        checkIn: makeDate(checkInOffset),
        checkOut: makeDate(checkInOffset + nights),
        nights,
        status,
        paymentStatus,
        amount,
      };
    });
    await Booking.insertMany(bookings, { ordered: false });
  }
};

app.listen(port, () => {
  console.log(`listing on port ${port}....`);
});

app.get("/assets/hotel-image.svg", (req, res) => {
  const seed = String(req.query.seed || "hotelops");
  const width = Math.max(320, Math.min(2400, Number(req.query.w || 1600)));
  const height = Math.max(240, Math.min(1800, Number(req.query.h || 900)));

  const hash = (input) => {
    let value = 5381;
    for (let i = 0; i < input.length; i++) value = (value * 33) ^ input.charCodeAt(i);
    return value >>> 0;
  };

  const h = hash(seed);
  const hueA = h % 360;
  const hueB = (hueA + 38 + (h % 44)) % 360;

  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="hsl(${hueA} 62% 52%)"/>
      <stop offset="1" stop-color="hsl(${hueB} 56% 38%)"/>
    </linearGradient>
    <radialGradient id="r" cx="20%" cy="18%" r="80%">
      <stop offset="0" stop-color="rgba(185,137,57,0.55)"/>
      <stop offset="1" stop-color="rgba(0,0,0,0)"/>
    </radialGradient>
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" stitchTiles="stitch" />
      <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.14 0"/>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <rect width="100%" height="100%" fill="url(#r)"/>
  <rect width="100%" height="100%" filter="url(#grain)" opacity="0.35"/>
  <g font-family="Outfit, system-ui, -apple-system, Segoe UI, Arial" fill="rgba(255,255,255,0.92)">
    <text x="${Math.round(width * 0.06)}" y="${Math.round(height * 0.78)}" font-size="${Math.round(
    height * 0.06
  )}" font-weight="800" letter-spacing="0.06em">HOTELOPS</text>
    <text x="${Math.round(width * 0.06)}" y="${Math.round(height * 0.84)}" font-size="${Math.round(
    height * 0.028
  )}" opacity="0.88">Hotel management • Front desk • Housekeeping</text>
  </g>
</svg>`;

  res.set("Cache-Control", "public, max-age=0");
  res.type("image/svg+xml").send(svg);
});



app.get("/login", (req, res) => {
  res.render("page/login_admin", { error: null, username: "" });
});

// for login verification of admin users 
app.post("/login", async (req, res) => {
  const user = String(req.body?.username || "").trim();
  const pass = String(req.body?.password || "").trim();

  if (!user || !pass) {
    return res.status(400).render("page/login_admin", {
      error: "Please enter both username and password.",
      username: user,
    });
  }

  try {
    const foundAdmin = await admin.findOne({ username: user });

    if (!foundAdmin) {
      return res.status(401).render("page/login_admin", {
        error: "Invalid username or password.",
        username: user,
      });
    }

    if (foundAdmin.password !== pass) {
      return res.status(401).render("page/login_admin", {
        error: "Invalid username or password.",
        username: user,
      });
    }

    req.session.isAdmin = true;
    req.session.adminUser = foundAdmin.username;
    return res.redirect("/admin");
  } catch (err) {
    console.error(err);
    return res.status(500).render("page/login_admin", {
      error: "Something went wrong. Please try again.",
      username: user,
    });
  }
});

app.get("/admin", requireAdmin, async (req, res) => {
  const rooms = await Room.find().sort({ number: 1 }).limit(18).lean();
  const bookingsRaw = await Booking.find().sort({ createdAt: -1 }).limit(10).lean();

  const bookings = bookingsRaw.map((b) => ({
    ...b,
    id: b.bookingId,
    checkIn: new Date(b.checkIn).toISOString().slice(0, 10),
    checkOut: new Date(b.checkOut).toISOString().slice(0, 10),
  }));

  const stats = {
    occupancy: rooms.length
      ? Math.round((rooms.filter((r) => r.status === "Occupied").length / rooms.length) * 100)
      : 0,
    available: rooms.filter((r) => r.status === "Available").length,
    arrivals: bookingsRaw.filter((b) => b.status === "Confirmed").length,
    pendingPayments: bookingsRaw.filter((b) => b.paymentStatus === "Pending").length,
  };

  res.render("page/adminPage", {
    nav: "admin",
    adminUser: req.session?.adminUser,
    stats,
    bookings,
    rooms,
  });
});

app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.clearCookie("connect.sid");
    res.redirect("/login");
  });
});


// home page front page of website
app.get("/", (req, res) => {
  const branchPool = [
    { city: "Mumbai", area: "Bandra West" },
    { city: "Delhi", area: "Connaught Place" },
    { city: "Bengaluru", area: "Indiranagar" },
    { city: "Hyderabad", area: "Hitech City" },
    { city: "Pune", area: "Koregaon Park" },
    { city: "Jaipur", area: "C-Scheme" },
    { city: "Kolkata", area: "Park Street" },
  ];

  const branches = branchPool
    .slice()
    .sort(() => Math.random() - 0.5)
    .slice(0, randomInt(3, 5))
    .map((b) => ({
      ...b,
      phone: `+91 ${randomInt(70000, 99999)} ${randomInt(10000, 99999)}`,
      rating: randomFloat(4.1, 4.9, 1),
    }));

  const imageSeeds = [
    "hotel-exterior",
    "hotel-lobby",
    "hotel-room",
    "boutique-hotel",
    "luxury-hotel",
    "hotel-reception",
  ];
  const sig = randomInt(10_000, 99_999);
  const imageUrl = (seed, w = 1600, h = 900) =>
    `/assets/hotel-image.svg?seed=${encodeURIComponent(
      `${seed}-${sig}`
    )}&w=${w}&h=${h}`;

  const hotel = {
    name: pick(["HotelOps Grand", "HotelOps Residency", "HotelOps Suites"]),
    tagline: pick([
      "Comfort-forward stays for modern travelers.",
      "A calm base for business and weekend getaways.",
      "City-center hospitality with warm service.",
    ]),
    heroImage: imageUrl(pick(imageSeeds)),
    gallery: [
      imageUrl("hotel-lobby", 800, 600),
      imageUrl("hotel-room", 800, 600),
      imageUrl("hotel-restaurant", 800, 600),
    ],
    rating: randomFloat(4.2, 4.9, 1),
    reviews: randomInt(140, 2800),
    hq: pick(branchPool),
    priceRange: pick(["₹₹", "₹₹₹", "₹₹₹₹"]),
    checkIn: "2:00 PM",
    checkOut: "11:00 AM",
    founded: randomInt(2008, 2022),
    highlights: [
      pick(["24/7 front desk", "Airport transfers", "Express check-in/out"]),
      pick(["Rooftop dining", "Conference rooms", "Co-working lounge"]),
      pick(["Family rooms", "Fitness studio", "Spa & wellness"]),
    ],
    amenities: [
      "Free Wi‑Fi",
      "Breakfast included",
      "Housekeeping",
      "Laundry service",
      "Parking",
      "Room service",
      "CCTV & security",
    ],
  };

  res.render("page/home", { hotel, branches });
});


app.get("/contact", (req, res) => {
  res.render("page/contact");
});
