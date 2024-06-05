# ![E-BabIfOoT](/assets/logo.png)

E-BabIfOoT is a project made during the IoT course designed to automate scorekeeping in a babyfoot game. Utilizing Arduino, Raspberry Pi, sensors, and wireless BLE technology, this system accurately counts and records scores, storing them in a database. It features a web interface for displaying real-time game information and another for monitoring the scores.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [Authors](#authors)

## Overview

The E-BabIfOoT project uses two Arduinos equipped with piezoelectric sensors placed in the goals to detect when a goal is scored. The data is then sent via BLE to a Raspberry Pi, which acts as the controller and display unit. The Raspberry Pi runs two webservers: one for displaying game information and another for listening to score updates.

## Features

- **Automatic Scorekeeping**: Real-time score detection using piezoelectric sensors.
- **Wireless Communication**: BLE for reliable, wireless data transmission.
- **Data Storage**: Score data is stored in a database for future reference.
- **Web Interface**: Accessible web interface to display game information and monitor scores.
- **Centralized Control**: Raspberry Pi acts as the central controller and display unit.

## Hardware Requirements

- 2 x Arduino MKR 1010 Wifi
- 1 x Raspberry Pi
- 2 x Piezoelectric sensors
- 1 x LCD touch screen for Raspberry Pi
- 1 x Babyfoot table
- 3D printed parts
- Batteries or power supply for the devices

## Software Requirements

- Arduino IDE
- Python 3.x
- Flask (for the webserver)
- SQLite (or any other preferred database)
- BLE libraries for Python (e.g., `pybluez`)

## Architecture

The system consists of two main components: the Arduino-based score detection system and the Raspberry Pi-based controller. The Arduinos are responsible for detecting goals and sending the data to the Raspberry Pi via BLE. The Raspberry Pi runs two webservers: one for displaying game information and another for listening to score updates. The system also includes a database to store the scores for future reference.

![System Architecture](/assets/architecture.png)

## Installation

1. **Arduino Setup:**
    - Connect the piezoelectric sensors to the Arduinos.
    - Upload the Arduino sketch to detect goals and send data via BLE.

2. **Raspberry Pi Setup:**
    - Install the required libraries and dependencies:

      ```sh
      sudo apt-get update
      sudo apt-get install python3-pip
      pip3 install flask pybluez sqlite3
      ```

    - Clone the repository:

      ```sh
      git clone https://github.com/kylianmanzini/IoT-Babyfoot/
      ```

3. **Running the Webservers:**
    - Start the webservers using the bash script:

      ```sh
      ./babyfoot_startup.sh
      ```

## Usage

1. **Starting a Game:**
    - Power on the Arduinos and Raspberry Pi.
    - Start and open the web interface on a browser to view the game information.

2. **Playing the Game:**
    - Start playing the babyfoot game.
    - The system will automatically detect and update the scores in real-time.

3. **Ending the Game:**
    - Use the interface button when the game is over.
    - The scores will be stored in the database for future reference.

## Future Improvements

- Add support for tournaments.
- Cloud integration for storing data.
- Implement user authentication for tracking player scores.
- Integrate with a mobile app for user auth.
- ... and much more!

## Authors

- Bastien Pillonel - [GitHub](https://github.com/Bastien18)
- Loïc Brasey - [GitHub](https://github.com/Brasey-on-github)
- Patrick Maillard - [GitHub](https://github.com/Patrick2ooo)
- Kylian Manzini - [GitHub](https://github.com/kylianmanzini)
