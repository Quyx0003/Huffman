import sys
from bitIO import BitReader
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

def read_frequencies(reader):
    freq = []
    for _ in range(256):
        freq.append(reader.readint32bits())
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

def decode_file(input_filename, output_filename, huffman_tree, original_size):
    reader = BitReader(open(input_filename, 'rb'))
    
    # Skip frequencies, they are already read
    for _ in range(256):
        reader.readint32bits()
    
    with open(output_filename, 'wb') as out:
        node = huffman_tree
        bytes_written = 0
        while bytes_written < original_size:
            bit = reader.readbit()
            if bit == 0:
                node = node.left
            else:
                node = node.right
            if node.byte != -1:
                out.write(bytes([node.byte]))
                node = huffman_tree
                bytes_written += 1
    reader.close()

def main(input_filename, output_filename):
    reader = BitReader(open(input_filename, 'rb'))
    freq = read_frequencies(reader)
    
    huffman_tree = build_huffman_tree(freq)

    original_size = sum(freq)
    decode_file(input_filename, output_filename, huffman_tree, original_size)
    reader.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Decode.py nameOfCompressedFile nameOfDecodedFile")
    else:
        main(sys.argv[1], sys.argv[2])
