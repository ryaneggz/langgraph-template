#!/bin/bash

export VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

# Install build tools if you haven't already
uv pip install --upgrade build twine

# Build the package
python -m build

# Upload to TestPyPI first (optional but recommended)
# python -m twine upload --non-interactive --repository testpypi dist/* --verbose

# Upload to PyPI
python -m twine upload dist/* --verbose

rm -rf dist
rm -rf build
rm -rf '*.egg-info'

echo "Version $VERSION published successfully."