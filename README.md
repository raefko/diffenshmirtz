# Diffenshmirtz

<img src="logo.webp" alt="image" width="50%" height="auto" style="display: block; margin: 0 auto">


**Diffenshmirtz** is a versatile tool for comparing files across two directories. It offers both a graphical user interface (GUI) and a command-line interface (CLI) to suit different needs. With Diffenshmirtz, you can easily identify unique files in each directory, compare file differences, and view these differences in a user-friendly format.

## Features

- **Graphical User Interface (GUI)**: Interactive tabs for unique files and file differences.
- **Command-Line Interface (CLI)**: Run the tool without the GUI and view results directly in the terminal.
- **Customizable File Extensions**: Specify which file extensions to include in the comparison.
- **Modern Look and Feel**: Clean and user-friendly interface.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/diffenshmirtz.git
    ```

2. Navigate to the project directory:
    ```bash
    cd diffenshmirtz
    ```

3. Ensure you have Python 3 installed. Install required lib using:
    ```bash
    ## ARCH
    sudo pacman -S tk
    ## Ubuntu/Debian
    sudo apt install python3-tk
    ```

## Usage

### GUI Mode

To run the tool with the GUI, use:
```bash
python differ_gui.py --dir1 path/to/dir1 --dir2 path/to/dir2 --extensions py,txt
```

### CLI Mode

**TODO**