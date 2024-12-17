const express = require("express");
const app = express();

app.use(express.json());

// In-memory "database"
let users = [
    { id: 1, name: "Rahim Bhai" },
    { id: 2, name: "Karim Bhai" }
];

// READ (GET): Get all users
app.get("/users", (req, res) => {
    res.status(200).json(users);
});

// READ (GET): Get a single user by ID
app.get("/users/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const user = users.find(u => u.id === id);
    if (user) {
        res.status(200).json(user);
    } else {
        res.status(404).json({ error: "User not found" });
    }
});

// CREATE (POST): Add a new user
app.post("/users", (req, res) => {
    const { name } = req.body;
    if (!name) {
        return res.status(400).json({ error: "Name is required" });
    }

    const newUser = { id: users.length + 1, name };
    users.push(newUser);
    res.status(201).json(newUser);
});

// UPDATE (PUT): Update a user's name by ID
app.put("/users/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const user = users.find(u => u.id === id);

    if (!user) {
        return res.status(404).json({ error: "User not found" });
    }

    const { name } = req.body;
    if (!name) {
        return res.status(400).json({ error: "Name is required" });
    }

    user.name = name;
    res.status(200).json(user);
});

// DELETE (DELETE): Remove a user by ID
app.delete("/users/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const userIndex = users.findIndex(u => u.id === id);

    if (userIndex === -1) {
        return res.status(404).json({ error: "User not found" });
    }

    users.splice(userIndex, 1);
    res.status(200).json({ message: "User deleted successfully" });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
