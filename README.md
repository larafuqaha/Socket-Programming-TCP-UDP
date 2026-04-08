# Socket Programming — TCP Web Server & UDP Trivia Game

A Python project developed as part of the Computer Networks course. It implements a multithreaded TCP web server and a real-time multiplayer UDP trivia game using socket programming.

## Overview

The project consists of two parts: a web server that handles HTTP requests and serves static content, and a UDP-based trivia game where multiple clients compete in real time.

## Part 1 — TCP Web Server (`server_TCP.py`)

A multithreaded HTTP web server that handles concurrent client connections using Python's `threading` module.

### Features
- Serves static HTML/CSS pages in both English and Arabic
- Handles common URL paths (`/`, `/en`, `/ar`, `/index.html`, etc.)
- Serves local image (`.jpg`, `.png`) and video (`.mp4`) files
- Redirects missing images to a Google Images search (307 Temporary Redirect)
- Redirects missing videos to a YouTube search (307 Temporary Redirect)
- Returns a custom 404 error page that displays the client's IP address and port
- Handles up to 20 concurrent connections

### How to Run
```bash
python server.py
```
Then open a browser and navigate to `http://<server-ip>:5698`

### Required Files
The following files must be in the same directory as `server_TCP.py`:
- `main_en.html` — English main page
- `main_ar.html` — Arabic main page
- `supporting_material_en.html` — English supporting material page
- `supporting_material_ar.html` — Arabic supporting material page
- `Error_404.html` — Custom 404 error page
- `style_main.css` — Stylesheet
- Any local image/video files to be served

> Note: Team member photos are not included in this repository.

## Part 2 — UDP Trivia Game (`server_UDP.py` & `client_UDP.py`)

A real-time multiplayer trivia game using UDP sockets. The server broadcasts questions to all connected clients, collects answers, calculates scores, and announces winners.

### Features
- Supports multiple simultaneous players
- Requires at least 2 players to start
- 3 randomly selected questions per round
- Score based on answer correctness and response speed
- Live leaderboard broadcast after each question
- Inactive players are removed after a round
- Players can type `exit` to leave the game

### How to Run

**Start the server:**
```bash
python server_UDP.py
```

**Start a client (run on each player's machine):**
```bash
python client_UDP.py
```
The client will prompt for the server IP, port number (`5689`), and a username.


## Team

- Lara Fuqaha
- Veronica Wakileh
- Fadi Bassous

