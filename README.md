# Middle Earth Trading Platform

Welcome to the Middle Earth Trading Platform! This platform is designed to facilitate trading of weapons among players
in the fantasy world of Middle Earth. Whether you're an elf, dwarf, hobbit, wizard, or any other race, this platform
provides a convenient way to exchange weapons and items with other players.

## Features

- **User Management**: Create, view, update, and delete user accounts.
- **Inventory Management**: Manage your inventory of weapons and items.
- **Offer Management**: Make and respond to trade offers from other players.
- **Flexible Configuration**: Easily configure database settings and environment variables.

## Installation

1. Clone the repository:
    - git clone https://github.com/Gauro/middle_earth_trading_platform.git

2. Install dependencies:

    - cd middle-earth-trading-platform
    - pip install -r requirements.txt

3. Set up the database:

    - Configure `config.ini` file in the `data` folder with your database settings.
    - import db_script.sql in mysql to import the schema with the required tables.
    - run sample_data.py for populating the database with dummy data.

## Usage

1. Start the FastAPI server:
    - run main.py

2. Access the API documentation:
    - Open your browser and go to `http://localhost:8000/docs`.

3. Explore the available endpoints for user management, inventory management, and offer management.

