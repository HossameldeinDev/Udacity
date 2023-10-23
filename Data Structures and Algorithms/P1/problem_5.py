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

        # We're including not just the data, but also the timestamp and the previous hash in the calculation.
        # This makes our hash dependent on the block's full contents.
        hash_str = f"{self.timestamp}{self.data}{self.previous_hash}".encode('utf-8')
        sha.update(hash_str)

        return sha.hexdigest()
    def is_valid(self):
        """
        Validates the block's data integrity. If the data has been altered since the
        block's creation, this will return False.
        """
        return self.calc_hash() == self.hash

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

    def validate_chain(self):
        # Start from the first block (genesis block) and go through the chain.
        for i in range(len(self.chain)):
            current_block = self.chain[i]

            # Check if the block's hash is still valid with the current data.
            if not current_block.is_valid():  # Utilizing the Block's own validation method.
                print(f"Block {i} has been tampered with.")
                return False

            # If we are not at the first block, check the link with the previous one.
            if i > 0:
                previous_block = self.chain[i - 1]
                if current_block.previous_hash != previous_block.hash:
                    print(f"Block {i} previous hash does not match with Block {i - 1} hash.")
                    return False

        return True


if __name__ == "__main__":
    blockchain = Blockchain()

    # Test Case 1: Adding a normal block
    data = "This is a regular block"
    print(f"Adding block with data: '{data}'")
    blockchain.add_block(data)
    # Expected output: Adding block with data: 'This is a regular block'

    # Test Case 2: Adding a block with None data (Edge Case)
    print("Adding block with None data")
    blockchain.add_block(None)
    # Expected output: Cannot add block with empty data

    # Test Case 3: Adding a block with empty string data (Edge Case)
    print("Adding block with empty string")
    blockchain.add_block('')
    # Expected output: Cannot add block with empty data

    # Test Case 4: Verifying the integrity of the blockchain
    print("Verifying blockchain integrity")
    is_valid = blockchain.validate_chain()  # Assuming there is a method to validate the chain.
    print(f"Is blockchain valid? {is_valid}")
    # Expected output: Is blockchain valid? True

    # Test Case 5: Adding an unusually large block (Edge Case)
    large_data = 'X' * 100  # Simulating 1MB of data
    print("Adding block with large data")
    blockchain.add_block(large_data)
    # Expected output: Block added successfully

    # Test Case 6: Attempting to tamper with a block (Edge Case)
    print("Tampering with the blockchain by altering a block's data")
    if len(blockchain.chain) > 0:
        blockchain.chain[0].data = "Tampered Data"  # Directly altering block data
        tamper_test = blockchain.validate_chain()  # Re-validating the chain
        print(f"Is blockchain valid after tampering? {tamper_test}")
    # Expected output: Is blockchain valid after tampering? False