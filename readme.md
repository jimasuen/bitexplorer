# Block Header Analyser

A simple python GUI for analysing Bitcoin block header structure.

## Features:
- Use with regtest or signet
- Displays total number of blocks
- Extracts version, previous block hash, Merkle root, timestamp, target, and nonce
- Converts the timestamp to a human-readable format

## Installation:
- Clone repo
- Navigate to the project directory: `cd bitexplorer`
- Install dependencies: `pip install -r requirements.txt`
- Rename `sample-config.yml` to `config.yml` or copy contents to a `config.yml` and update it with your Bitcoin Core details

## Usage:
In the terminal, run `python bitexplorer/main.py`

## Requirements:
- Python 3.x
- py-bitcoinkernel
- PyYAML