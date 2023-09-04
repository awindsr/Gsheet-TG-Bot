# Gsheet-TG-Bot

**Gsheet-TG-Bot** is a Telegram bot that enables interaction with Google Sheets directly from your Telegram chat. With this bot, you can query data, update sheets, and perform various actions on your Google Sheets without leaving Telegram.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Query Data**: Retrieve data from your Google Sheets by specifying criteria.
- **Update Sheets**: Make changes to your Google Sheets, such as updating cell values.
- **Custom Commands**: Create custom commands to perform specific actions on your sheets.
- **Data Privacy**: Your data stays within the Telegram ecosystem, ensuring privacy and security.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/awindsr/Gsheet-TG-Bot.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a Telegram bot and obtain your bot's API token. Refer to [Telegram's BotFather documentation](https://core.telegram.org/bots#botfather) for instructions.

4. Create a Google Sheets API project and obtain your API credentials JSON file. You can follow Google's [Sheets API Quickstart guide](https://developers.google.com/sheets/api/quickstart) for setup.

5. Set up your configuration by editing the `config.py` file. Provide your Telegram bot token and the path to your Google Sheets API credentials JSON file.

6. Run the bot:

   ```bash
   python main.py
   ```

7. Start a chat with your Telegram bot and begin interacting with your Google Sheets!

## Usage

1. Start a chat with your Telegram bot by searching for its username.

2. Send commands and queries in the chat to interact with your Google Sheets.

3. The bot will respond with the requested data or perform the specified actions on your Google Sheets.

## Commands

- `/add row col data`: Add data to your Google Sheets.
- `/list`: List all student names with roll numbers.
- `/check rollnumber`: List the entries of a specific student.
- `/del row col`: Delete data from your Google Sheets.
- `/total collected col`: Get the total amount collected for a specific need.

## Contributing

Contributions are welcome! If you'd like to contribute to the development of Gsheet-TG-Bot, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test thoroughly.
4. Create a pull request to the `main` branch of this repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to reach out to the project owner for any questions or support.

Enjoy using Gsheet-TG-Bot!
```
