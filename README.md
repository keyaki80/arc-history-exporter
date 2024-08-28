# Arc Browser History Exporter

This Python script exports the browsing history from the Arc browser within a specified date range. The exported data is saved as a CSV file on the user's desktop.

## Features

- Export Arc browser history for a specified date range
- Save the history as a CSV file on the desktop
- Simple command-line interface

## Requirements

- Python 3.6 or higher
- Arc browser installed on macOS

## Installation

1. Clone this repository or download the script file.
2. Ensure you have Python 3.6 or higher installed on your system.

## Usage

Run the script from the command line with optional arguments:

```
python arc_history_exporter.py [--start START] [--end END]
```

Arguments:
- `--start`: Start date (integer). 0 for today, -1 for yesterday, etc. Default is 0 (today).
- `--end`: End date (integer). Same format as start. Default is 0 (end of today).

If no arguments are provided, the script will export the history for the current day (from 00:00 to 23:59).

Examples:
```
# Export today's history
python arc_history_exporter.py

# Export history for the past 7 days
python arc_history_exporter.py --start -7 --end 0

# Export history from 3 days ago to yesterday
python arc_history_exporter.py --start -3 --end -1
```

## Output

The script will create a CSV file on your desktop with the naming format:
`arc_history_YYYYMMDD_YYYYMMDD.csv`

The CSV file contains the following columns:
1. ID
2. Visit Time
3. Title
4. URL

## Note

This script is designed for use with the Arc browser on macOS. Ensure you have the necessary permissions to access the browser's history file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

For more information about the MIT License, you can visit:
[Open Source Initiative - MIT License](https://opensource.org/licenses/MIT)

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/Kensei/arc-history-exporter/issues) if you want to contribute.

## Author

Kensei (@fullen789)

You can find me on X (formerly Twitter): [@fullen789](https://x.com/fullen789)
