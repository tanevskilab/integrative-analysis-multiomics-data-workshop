#!/usr/bin/env bash
set -Eeuo pipefail

# Start JupyterLab using /mnt/data for writable runtime, cache,
# configuration, plotting cache, and temporary files.
#
# Usage:
#   ./start-jupyter-data.sh
#   ./start-jupyter-data.sh /mnt/data/practical2
#
# Default Jupyter root:
#   /mnt/data
#
# Per-user working directory:
#   /mnt/data/<username>/jupyter

JUPYTER_BIN="${JUPYTER_BIN:-/usr/local/share/course/bin/jupyter-lab}"
NOTEBOOK_DIR="${1:-/mnt/data}"
BASE="${JUPYTER_BASE:-/mnt/data/${USER}/jupyter}"

# Ensure newly created user-specific files are private.
umask 077

pause_on_exit() {
    status=$?

    echo
    if (( status == 0 )); then
        echo "JupyterLab stopped."
    else
        echo "JupyterLab exited with status: $status"
    fi

    if [[ -t 0 ]]; then
        read -r -p "Press Enter to close this terminal..." || true
    fi
}

trap pause_on_exit EXIT

if [[ ! -x "$JUPYTER_BIN" ]]; then
    echo "Error: JupyterLab executable was not found or is not executable:"
    echo "  $JUPYTER_BIN"
    exit 1
fi

if [[ ! -d "$NOTEBOOK_DIR" ]]; then
    echo "Error: notebook directory does not exist:"
    echo "  $NOTEBOOK_DIR"
    exit 1
fi

if [[ ! -r "$NOTEBOOK_DIR" || ! -x "$NOTEBOOK_DIR" ]]; then
    echo "Error: notebook directory is not accessible:"
    echo "  $NOTEBOOK_DIR"
    exit 1
fi

# Create separate writable directories for the current user.
mkdir -p \
    "$BASE/runtime" \
    "$BASE/tmp" \
    "$BASE/config" \
    "$BASE/data" \
    "$BASE/cache" \
    "$BASE/ipython" \
    "$BASE/matplotlib"

chmod 700 \
    "$BASE" \
    "$BASE/runtime" \
    "$BASE/tmp" \
    "$BASE/config" \
    "$BASE/data" \
    "$BASE/cache" \
    "$BASE/ipython" \
    "$BASE/matplotlib"

# Redirect Jupyter, IPython, Matplotlib, XDG, and temporary files
# away from the full root filesystem.
export JUPYTER_RUNTIME_DIR="$BASE/runtime"
export JUPYTER_CONFIG_DIR="$BASE/config"
export JUPYTER_DATA_DIR="$BASE/data"

export XDG_CONFIG_HOME="$BASE/config"
export XDG_DATA_HOME="$BASE/data"
export XDG_CACHE_HOME="$BASE/cache"

export MPLCONFIGDIR="$BASE/matplotlib"
export IPYTHONDIR="$BASE/ipython"
export TMPDIR="$BASE/tmp"

echo "Starting JupyterLab"
echo
echo "User:                 $USER"
echo "Jupyter root:         $NOTEBOOK_DIR"
echo "User data directory:  $BASE"
echo "Runtime directory:    $JUPYTER_RUNTIME_DIR"
echo "Temporary directory:  $TMPDIR"
echo "Matplotlib directory: $MPLCONFIGDIR"
echo
echo "Keep this terminal open."
echo "Copy the displayed http://localhost:... URL into your browser."
echo
echo "Linux permissions still control which directories can be opened"
echo "or modified under $NOTEBOOK_DIR."
echo

"$JUPYTER_BIN" \
    --no-browser \
    --ServerApp.root_dir="$NOTEBOOK_DIR"