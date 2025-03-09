from pathlib import Path
from config import Config
from typing import List

import tkinter as tk
import pbk
import datetime

config_path = Path(__file__).resolve().parent.parent / "config.yml"
config = Config(str(config_path))

datadir = config.datadir
network_mapping = {
    "regtest": pbk.ChainType.REGTEST,
    "signet": pbk.ChainType.SIGNET
}

chaintype = network_mapping.get(config.network.lower())
chainman = pbk.load_chainman(datadir, chaintype)

blocks = pbk.block_index_generator(chainman, 1)
total_blocks = sum(1 for _ in blocks)

root = tk.Tk()
root.geometry("700x900")
root.title("Block Header Analyser")

block_height = tk.IntVar()


def clear_input(widgets: List):
    for widget in widgets:
        widget.config(state="normal")
        if isinstance(widget, tk.Text):
            widget.delete(1.0, tk.END)
        else:
            widget.delete(0, tk.END)


def fetch_block():

    clear_input([
        block_hash_entry,
        text_area,
        bh_version_entry,
        bh_prev_entry,
        bh_merkle_entry,
        bh_timestamp_entry,
        bh_target_entry,
        bh_nonce_entry
        ])

    try:
        height = block_height.get()

        if height < 0:
            raise ValueError("Height must be a positive number")

        block_index = pbk.block_index_generator(chainman, height, height)
        block_data = chainman.read_block_from_disk(next(block_index, None))

        message_label.config(text="Block found", foreground="green")

        # raw data breakdown
        block_hash = block_data.hash
        version = block_data.data[:4][::-1]
        prev_block_hash = block_data.data[4:36][::-1]
        merkle_root = block_data.data[36:68][::-1]
        timestamp = block_data.data[68:72][::-1]
        target = block_data.data[72:76][::-1]
        nonce = block_data.data[76:80][::-1]

        # format parts of the data readable
        timestamp_int = int(timestamp.hex(), 16)
        format_timestamp = datetime.datetime.fromtimestamp(timestamp_int, datetime.UTC)

        # cur block hash      
        block_hash_entry.insert(tk.END, bytes.fromhex(block_hash.hex)[::-1].hex())
        block_hash_entry.config(state="readonly")
        
        # raw data
        text_area.config(state="normal")
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, block_data.data.hex())
        text_area.config(state="disabled")

        # version
        bh_version_entry.insert(tk.END, version.hex())
        bh_version_entry.config(state="readonly")

        # previous block hash
        bh_prev_entry.insert(tk.END, prev_block_hash.hex())
        bh_prev_entry.config(state="readonly")

        # merkle root
        bh_merkle_entry.insert(tk.END, merkle_root.hex())
        bh_merkle_entry.config(state="readonly")

        # timestamp
        bh_timestamp_entry.insert(tk.END, f"Hex: {timestamp.hex()} / As int: {timestamp_int} / Readable: {format_timestamp}")
        bh_timestamp_entry.config(state="readonly")

        # target
        bh_target_entry.insert(tk.END, target.hex())
        bh_target_entry.config(state="readonly")

        # nonce
        bh_nonce_entry.insert(tk.END, nonce.hex())
        bh_nonce_entry.config(state="readonly")

    except Exception as e:
        message_label.config(text=f"Error: {e}" , foreground="red")
        print(f"Error: {e}")
        return

total_label = tk.Label(root, text=f"Total number of blocks: {total_blocks}", font=("calibre", 20, "bold"))  
total_label.pack(pady=10)

# input box
height_input_frame = tk.Frame(root)
height_input_frame.pack(pady=10)

height_label = tk.Label(height_input_frame, text="Enter block height: ")
height_label.pack(side="left", padx=5)
entry = tk.Entry(height_input_frame, textvariable=block_height)
entry.pack(side="left", padx=5)
button = tk.Button(height_input_frame, text="Fetch Block", command=fetch_block)
button.pack(side="left",padx=5)

message_label = tk.Label(root, text="")
message_label.pack(pady=10)

# cur block hash
block_hash_label = tk.Label(root, text="Current block hash:", justify="left")
block_hash_label.pack(pady=5, anchor="w", padx=10)
block_hash_entry = tk.Entry(root, textvariable="")
block_hash_entry.pack(fill="x", expand=False, padx=10, pady=5)

# for raw block data
raw_data_label = tk.Label(root, text="Raw block data in hex:", justify="left")
raw_data_label.pack(pady=5, anchor="w", padx=10)
text_area = tk.Text(root, wrap="word", height=10, width=80, bd=1, relief="solid")
text_area.pack(fill="x", expand=False, padx=10, pady=5)

block_header_frame = tk.Frame(root)
block_header_frame.pack(fill="x", pady=5, padx=10)

block_header_label = tk.Label(block_header_frame, text="Block header structure", font=("calibre", 15, "bold"))  
block_header_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

label_width = 10  

# for version hex
bh_version_label = tk.Label(block_header_frame, text="Version:", width=label_width, anchor="w")
bh_version_label.grid(row=1, column=0, padx=5, pady=5)
bh_version_entry = tk.Entry(block_header_frame)
bh_version_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# for previous hash hex
bh_prev_label = tk.Label(block_header_frame, text="Prev. hash:", width=label_width, anchor="w")
bh_prev_label.grid(row=2, column=0, padx=5, pady=5)
bh_prev_entry = tk.Entry(block_header_frame)
bh_prev_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# for merkle root hex
bh_merkle_label = tk.Label(block_header_frame, text="Merkle root:", width=label_width, anchor="w")
bh_merkle_label.grid(row=3, column=0, padx=5, pady=5)
bh_merkle_entry = tk.Entry(block_header_frame)
bh_merkle_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# for timestamp hex
bh_timestamp_label = tk.Label(block_header_frame, text="Timestamp:", width=label_width, anchor="w")
bh_timestamp_label.grid(row=4, column=0, padx=5, pady=5)
bh_timestamp_entry = tk.Entry(block_header_frame)
bh_timestamp_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

# target hex
bh_target_label = tk.Label(block_header_frame, text="Target:", width=label_width, anchor="w")
bh_target_label.grid(row=5, column=0, padx=5, pady=5)
bh_target_entry = tk.Entry(block_header_frame)
bh_target_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

# nonce hex
bh_nonce_label = tk.Label(block_header_frame, text="Nonce:", width=label_width, anchor="w")
bh_nonce_label.grid(row=6, column=0, padx=5, pady=5)
bh_nonce_entry = tk.Entry(block_header_frame)
bh_nonce_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

block_header_frame.grid_columnconfigure(1, weight=1)

root.mainloop()