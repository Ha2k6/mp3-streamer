#!/bin/bash

# Download and set up Google Chrome
mkdir -p /opt/chrome
wget -qO- "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/linux_amd64.deb" > /opt/chrome/chrome.deb
dpkg-deb -x /opt/chrome/chrome.deb /opt/chrome/
ln -sf /opt/chrome/opt/google/chrome/google-chrome /usr/bin/google-chrome

# Download and set up ChromeDriver
mkdir -p /opt/chromedriver
wget -q "https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip" -O /opt/chromedriver/chromedriver.zip
unzip -q /opt/chromedriver/chromedriver.zip -d /opt/chromedriver/
chmod +x /opt/chromedriver/chromedriver
ln -sf /opt/chromedriver/chromedriver /usr/bin/chromedriver

# Start the Flask app
gunicorn -b 0.0.0.0:5000 app:app
