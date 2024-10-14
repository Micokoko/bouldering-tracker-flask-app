
---

# ROCK-A-PHILE

**ROCK-A-PHILE** is a bouldering management application built with Flask, styled using Tailwind CSS and Flowbite. The app allows users to log their bouldering ascents, view leaderboards, and for admins (or route setters) to create and manage boulders.

## Features

### 1. **User Authentication**
- Secure user registration and login functionality, built using Flask and SQLAlchemy ORM.
- Passwords are stored securely in the database using encryption (hashing).
- Users are authenticated based on their unique usernames and passwords.
- Flask-Login is used to manage user sessions, allowing users to securely log in and access restricted features.
- Users can edit their profiles, update profile pictures, and change account details.
  
### 2. **Admin/Route Setter Features**
- Admins can create, edit, and delete boulders.
- Each boulder contains attributes such as name, color, difficulty, number of moves, and a description.
- Route setters can manage boulders through a clean and responsive interface.

### 3. **Ascent Logging**
- Users can log their attempts on boulders, tracking:
  - Number of attempts.
  - Status of the ascent (incomplete, completed, or flashed).
  - Number of moves completed in the ascent.
- Users can view their personal logs to track their progress on different boulders.

### 4. **Leaderboards**
- Each ranked boulder has its own leaderboard, where climbers are ranked based on the number of attempts.
- The fewer the attempts, the higher the rank.
- Only completed or flashed ascents count towards leaderboard ranking.

### 5. **Responsive Design**
- Fully responsive design optimized for all devices using Tailwind CSS and Flowbite.
- The interface is user-friendly and adapts well across mobile, tablet, and desktop devices.

## ORM with SQLAlchemy

The app uses SQLAlchemy ORM to map the database tables to Python classes, making database interactions simple and efficient.

- **User Model**: Handles user details such as username, email, password, profile picture, and climbing stats like highest grade climbed and flashed.
- **Boulder Model**: Stores information about each boulder, including difficulty level, the number of moves, color, and the route setter who created it.
- **Attempt Model**: Logs user attempts on each boulder, including the number of attempts, the completion status (incomplete, completed, flashed), and the date of the attempt.

These models are connected through relationships, with users having multiple attempts and boulders being associated with their route setters.

## Tech Stack

- **Backend**: Flask
- **Frontend**: Tailwind CSS, Flowbite
- **Database**: SQLite (configurable for other databases)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rock-a-phile.git
   cd rock-a-phile
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

6. Access the app at `http://localhost:5000`

## Usage

- Users can register and log in to access the main features of the app.
- Admins can manage boulders and view the activity of all users.
- Users can log ascents, view leaderboards, and track their personal progress on various boulders.



---
