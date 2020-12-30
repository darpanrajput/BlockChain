# module one building block chain
# insatlle flask

import datetime  # each block will have its own time stamp
import hashlib  # to calculate the hash
import json  # https json response
from flask import Flask, jsonify  # for web site postman ,http request and jsonify to


# diplay the request and minig response to be send thorugh this json

# part1 building block chain

class Blockchain:
    def __init__(self):
        self.chain = []  # list containg blocks
        # genesis block
        self.create_block(proof=1, prev_hash='0')

    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': datetime.datetime.now(),
                 'proof': proof,
                 'prev_hash': prev_hash}

        self.chain.append(block)
        return block

    def get_prev_block(self):
        # to get the last block in the chain
        return self.chain[-1]  # last block of the chain

    def POW(self, previous_proof):
        new_proof = 1
        check_proof = False  # initally the proof was false and miner have to find the soltion of the block
        while check_proof is False:
            # problem is miners to soleve is SHA 256
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # sholud be nonsymetrical
            # check if the first four character are 4 leading the zero
            if hash_operation[:4] != '0000':
                # miner wins
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        # make our blocks as a string to
        # uing the jsond dump our block is the
        # th dictionary that actually is json dimp
        encoded_block = json.dumps(block, sort_keys=True).encode()
        # this format is expected by the sha 256 hash function
        return hashlib.sha256(encoded_block.hexdigest())

    def is_Chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            previous_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2)
                                            .encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True


from flask import Flask

app = Flask(__name__)
# creat blockchain

blockchain = Blockchain()


# part2 mining our block

@app.route('/min_block', methods=['GET'])
def min_block():
    prev_block = blockchain.get_prev_block
    previous_proof = prev_block['previous_proof']
    proof = blockchain.POW(previous_proof)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    response = {'message': "congratulation ypu have mined it!!",
                "index": block[index],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash']}
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                "length": len(blockchain.chain)}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
