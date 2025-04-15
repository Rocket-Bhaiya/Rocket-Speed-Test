# Rocket Speed Test

A modern and clean Internet Speed Test application built with PyQt5.

![Rocket Speed Test Screenshot](screenshot.png)

## Features

- **Clean, Modern UI**: Dark theme with flat buttons and rounded corners
- **Comprehensive Testing**: Measures download speed, upload speed, and ping
- **Responsive Design**: Progress bar animation shows test progress
- **Multithreaded**: UI remains responsive during tests
- **Error Handling**: Gracefully handles connection issues

## Requirements

- Python 3.x
- PyQt5
- speedtest-cli
- matplotlib (for optional graphing features)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rocket-speed-test.git
cd rocket-speed-test
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install PyQt5 speedtest-cli matplotlib
```

## Usage

Run the application:
```bash
python speed_test.py
```

- Click "Start Test" to begin testing your internet connection
- The progress bar will show the test progress
- Results will display download speed (Mbps), upload speed (Mbps), and ping (ms)
- Click "Refresh" to reset the application for a new test

## Development

The application is designed with a modular structure:

- `SpeedTestThread`: Handles network testing in a separate thread
- `RoundedWidget`: Custom widget with rounded corners for a modern look
- `SpeedTestApp`: Main application class that handles the UI and logic

## License

MIT License

## Author

Your Name

## Last Updated

April 15, 2025