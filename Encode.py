import sys
from bitIO import BitWriter
import PQHeap

class Element:
    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __lt__(self, other):
        return self.key < other.key

class HuffmanNode:
    def __init__(self, byte=-1, left=None, right=None):
        self.byte = byte
        self.left = left
        self.right = right

def calculate_frequencies(filename):
    freq = [0] * 256
    with open(filename, 'rb') as f:
        while byte := f.read(1):
            freq[byte[0]] += 1
    return freq

def build_huffman_tree(freq):
    pq = PQHeap.createEmptyPQ()
    for byte, f in enumerate(freq):
        if f > 0:
            PQHeap.insert(pq, Element(f, HuffmanNode(byte)))

    while len(pq) > 1:
        e1 = PQHeap.extractMin(pq)
        e2 = PQHeap.extractMin(pq)
        merged = HuffmanNode(left=e1.data, right=e2.data)
        PQHeap.insert(pq, Element(e1.key + e2.key, merged))

    return PQHeap.extractMin(pq).data

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = [""] * 256
    if node.byte != -1:
        codebook[node.byte] = prefix
    else:
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def write_frequencies(freq, writer):
    for f in freq:
        writer.writeint32bits(f)
    writer.flush()

def encode_file(input_filename, output_filename, codebook):
    with open(input_filename, 'rb') as input_file, open(output_filename, 'ab') as output_file:
        writer = BitWriter(output_file)
        while byte := input_file.read(1):
            code = codebook[byte[0]]
            for bit in code:
                writer.writebit(int(bit))
        writer.flush()

def main(input_filename, output_filename):
    freq = calculate_frequencies(input_filename)
    huffman_tree = build_huffman_tree(freq)
    codebook = generate_codes(huffman_tree)

    with open(output_filename, 'wb') as f:
        writer = BitWriter(f)
        write_frequencies(freq, writer)
        writer.close()

    encode_file(input_filename, output_filename, codebook)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Encode.py nameOfOriginalFile nameOfCompressedFile")
    else:
        main(sys.argv[1], sys.argv[2])
