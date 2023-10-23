import hashlib
import time


class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        # Convert the data to a string, regardless of its original type.
        hash_str = str(self.data).encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()



class Blockchain:
    def __init__(self):
        self.chain = []
        # Initialize the blockchain with the genesis block
        genesis_block = self.create_genesis_block()
        self.chain.append(genesis_block)

    def create_genesis_block(self):
        # Manually construct a block with
        # timestamp, data, previous_hash
        return Block(time.time(), "Genesis Block", "0")


    def get_latest_block(self):
        # Returns the most recent block in the chain
        return self.chain[-1] if self.chain else None

    def add_block(self, data):
        if not data:  # Check if the data is empty
            print("Cannot add block with empty data")
            return

        timestamp = time.time()
        previous_block = self.get_latest_block()
        previous_hash = previous_block.hash if previous_block else "0"  # for the genesis block
        new_block = Block(timestamp, data, previous_hash)

        self.chain.append(new_block)  # Append the new block to the chain



# Test cases

# Test case to handle edge cases, including null, empty, and very large values
if __name__ == "__main__":
    # Create a new Blockchain object
    blockchain = Blockchain()

    # Test Case 1: Attempt to add a block with None data
    print("Test Case 1:")
    blockchain.add_block(None)

    # Test Case 2: Attempt to add a block with empty data
    print("\nTest Case 2:")
    blockchain.add_block('')

    # Test Case 3: Add a regular block with valid data
    print("\nTest Case 3:")
    blockchain.add_block('Valid Block Data')

    # Test Case 4: Add a block with a large amount of data
    print("\nTest Case 4:")
    large_data = 'A' * (10**6)  # 1 million characters
    blockchain.add_block(large_data)

    # Test Case 5: Attempt to add a block with non-string data (e.g., integer, float, object)
    print("\nTest Case 5:")
    blockchain.add_block(12345)  # Passing an integer
    blockchain.add_block(123.45)  # Passing a float
    blockchain.add_block({"name": "test"})  # Passing a dictionary

    # Test Case 6: Attempt to add several blocks successively
    print("\nTest Case 6:")
    for i in range(5):
        blockchain.add_block(f"Consecutive block {i}")

    # Test Case 7: Attempt to manipulate the previous block's hash (integrity check)
    print("\nTest Case 7:")
    blockchain.add_block('New Block Before Manipulation')
    if blockchain.chain:
        # Directly manipulate the hash of a block in the chain
        if len(blockchain.chain) > 1:
            blockchain.chain[-2].hash = 'manipulated_hash'
        blockchain.add_block('New Block After Manipulation')

    # Display the blockchain
    for i, block in enumerate(blockchain.chain):
        print(f"\nBlock {i} Details:")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")

    # Test Case 8: Attempt to add a block with very long string data, potentially causing a buffer overflow
    print("\nTest Case 8:")
    try:
        extremely_large_data = 'B' * (10**9)  # 1 billion characters
        blockchain.add_block(extremely_large_data)
    except Exception as e:
        print(f"An exception occurred: {e}")
