# python-data-viz

This project is designed to read the output JSON file from `game.py` and display a heat map along with relevant game information such as game mode, score, and reaction speed.

## Project Structure

```
python-data-viz
├── src
│   ├── main.py          # Entry point of the application
│   ├── visualization     # Module for visualization functions
│   │   ├── __init__.py
│   │   └── heatmap.py   # Functions to generate and display heat maps
│   ├── utils            # Module for utility functions
│   │   ├── __init__.py
│   │   └── json_reader.py # Functions to read and parse JSON data
│   └── config           # Module for configuration settings
│       ├── __init__.py
│       └── settings.py   # Configuration settings for the project
├── tests                # Module for unit tests
│   ├── __init__.py
│   └── test_json_reader.py # Unit tests for json_reader.py
├── requirements.txt     # List of dependencies
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-data-viz
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

This will read the JSON output from `game.py`, generate the heat map, and display the relevant game information.

## Testing

To run the tests, use the following command:
```
pytest tests/
```

This will execute the unit tests defined in `test_json_reader.py`.

## License

This project is licensed under the MIT License.