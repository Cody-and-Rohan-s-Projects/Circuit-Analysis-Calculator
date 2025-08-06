#!/bin/sh
# Create folders.
[ -e package ] && rm -r package
mkdir -p package/opt/CircuitAnalysis
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/256x256/apps

# Copy files.
cp -r CircuitAnalysis package/opt/CircuitAnalysis/
cp icon.png package/usr/share/icons/hicolor/256x256/apps
cp CircuitAnalysis.desktop package/usr/share/applications

# Change permissions.
chmod 755 package/opt/CircuitAnalysis/CircuitAnalysis
find package/usr/share -type f -exec chmod 644 {} +
