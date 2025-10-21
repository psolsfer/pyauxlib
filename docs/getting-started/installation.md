# Installation

## Using Package Managers

To install pyauxlib in your project, choose your preferred package manager:

=== "pip (simple install)"

    ```bash linenums="0"
    pip install pyauxlib
    ```

    The following [pip guide] can help getting started with [pip] usage.

=== ":simple-uv: uv (recommended for new projects)"

    First, install [uv] if you haven't already (for more detailed instructions refer to [uv installation] in the official documentation):

    ```bash linenums="0"
    # Windows (PowerShell)
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    # Linux/macOS
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Then create and initialize a new project:

    ```bash linenums="0"
    # Create project directory
    mkdir myproject && cd myproject

    # Initialize project with Python 3.10
    uv init --python 3.10

    # Install pyauxlib
    uv add pyauxlib
    ```

=== ":simple-poetry: Poetry"

    First, install [Poetry] if you haven't already (for more detailed instructions refer to [Poetry installation] in the official documentation):

    Then create and initialize a new project:

    ```bash linenums="0"
    # Create a new project
    poetry new myproject
    cd myproject

    # Set Python version
    poetry env use 3.10

    # Install pyauxlib
    poetry add pyauxlib
    ```

## Development Installation

To install pyauxlib for development:

```bash linenums="0"
git clone https://github.com/psolsfer/pyauxlib.git
cd pyauxlib
uv sync
```

This command installs all dependencies as specified in `pyproject.toml` and also creates a virtual environment if one doesn't exist.

[GitHub repo]: https://github.com/psolsfer/pyauxlib

[pip]: https://pip.pypa.io/en/stable/
[pip guide]: https://pip.pypa.io/en/stable/getting-started/
[Poetry]: https://python-poetry.org/
[Poetry installation]: https://python-poetry.org/docs/#installation
[uv]: https://docs.astral.sh/uv/
[uv installation]: https://docs.astral.sh/uv/getting-started/installation/#installation-methods
