
import json
import hashlib
import time
import os

# Constants
DIFFICULTY_TARGET = int("0000ffff00000000000000000000000000000000000000000000000000000000", 16)
MAX_BLOCK_SIZE = 1000000  # Maximum block size in bytes

def validate_transaction(transaction):
    # Step 1: Check if the transaction inputs refer to existing UTXOs
    for vin in transaction["vin"]:
        # Check if the txid of the input transaction exists in the blockchain (not implemented here)
        pass

    # Step 2: Verify that the sum of input values is greater than or equal to the sum of output values
    input_value = sum(vin["prevout"]["value"] for vin in transaction["vin"])
    output_value = sum(vout["value"] for vout in transaction["vout"])
    if input_value < output_value:
        return False

    # Step 3: Verify that the transaction inputs are correctly signed (not implemented here)

    # Step 4: Verify that the transaction outputs are correctly formatted (not implemented here)

    return True

# Function to calculate the hash of a block header
def calculate_block_hash(block_header):
    return hashlib.sha256(block_header.encode()).hexdigest()

# Function to mine a block
def mine_block(transactions):
    block = {
        "header": "",
        "coinbase_transaction": {},
        "transactions": []
    }

    # Create coinbase transaction
    coinbase_transaction = {
        "txid": "coinbase_txid"
        # Add other necessary fields
    }
    block["coinbase_transaction"] = coinbase_transaction
    block["transactions"].append(coinbase_transaction)

    block_size = len(json.dumps(coinbase_transaction))

    for transaction in transactions:
        if validate_transaction(transaction):
            transaction_size = len(json.dumps(transaction))
            if block_size + transaction_size <= MAX_BLOCK_SIZE:
                block["transactions"].append(transaction)
                block_size += transaction_size

    # Create block header
    block_header = json.dumps(block["transactions"]) + str(int(time.time())) + "nonce"

    # Mine the block
    nonce = 0
    while True:
        block_header_with_nonce = block_header + str(nonce)
        block_hash = calculate_block_hash(block_header_with_nonce)
        if int(block_hash, 16) < DIFFICULTY_TARGET:
            block["header"] = block_header_with_nonce
            break
        nonce += 1

    return block

# Function to read transaction data from JSON files
def read_transactions_from_files(folder_path):
    transactions = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                transaction = json.load(file)
                transactions.append(transaction)
    return transactions

# Function to write block data to output file
def write_block_to_file(block, output_file):
    with open(output_file, "w") as file:
        file.write(block["header"] + "\n")
        file.write(json.dumps(block["coinbase_transaction"]) + "\n")
        for transaction in block["transactions"]:
            file.write(transaction["txid"] + "\n")

def main():
    folder_path = "mempool"  # Path to the folder containing transaction JSON files
    output_file = "output.txt"

    # Read transactions from files
    transactions = read_transactions_from_files(folder_path)

    print("number of transactions: ", len(transactions))

    # Mine the block
    block = mine_block(transactions)

    # Write block data to output file
    write_block_to_file(block, output_file)

if __name__ == "__main__":
    main()
