#!/bin/bash
# build.sh

# Exit if any command fails
set -e

# Define source and build directories
SOURCE_DIR="src/handlers"
BUILD_DIR="build/lambda"

echo "Starting build process..."

# 1. Clean up previous build artifacts
echo "Cleaning up old build directory..."
rm -rf ./build

# 2. Create a new build directory
mkdir -p $BUILD_DIR

# 3. Use Poetry to export a requirements.txt file
echo "Exporting dependencies from Poetry..."
poetry --directory=$SOURCE_DIR export -f requirements.txt --output $BUILD_DIR/requirements.txt --without-hashes

# 4. Install dependencies into the build directory
echo "Installing dependencies with pip..."
pip install -r $BUILD_DIR/requirements.txt -t $BUILD_DIR

# 5. Copy your Lambda source code into the build directory
echo "Copying source code..."
cp -R $SOURCE_DIR/*.py $BUILD_DIR/

echo "Build complete. Artifacts are in $BUILD_DIR"