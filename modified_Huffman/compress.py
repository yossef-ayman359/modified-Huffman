from collections import Counter
import heapq
import math
from itertools import count

OTHERS_TOKEN = object()


def calculate_probabilities(text):
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if len(text) == 0:
        raise ValueError("Input text cannot be empty.")

    frequencies = Counter(text)
    total_symbols = len(text)

    probabilities = {
        symbol: frequency / total_symbols
        for symbol, frequency in frequencies.items()
    }

    return frequencies, probabilities


def group_symbols(probabilities, min_limit):
    if not isinstance(min_limit, (int, float)):
        raise TypeError("Minimum Limit must be a number.")

    if not math.isfinite(min_limit) or not 0 <= min_limit <= 1:
        raise ValueError("Minimum Limit must be between 0 and 1.")

    ordinary_symbols = {}
    others_symbols = {}

    for symbol, probability in probabilities.items():
        if probability <= min_limit:
            others_symbols[symbol] = probability
        else:
            ordinary_symbols[symbol] = probability

    grouped_probabilities = ordinary_symbols.copy()

    if others_symbols:
        grouped_probabilities[OTHERS_TOKEN] = sum(
            others_symbols.values()
        )

    return ordinary_symbols, others_symbols, grouped_probabilities


def generate_original_codes(symbols):
    symbols = sorted(symbols)

    if not symbols:
        return {}

    code_length = max(1, (len(symbols) - 1).bit_length())

    original_codes = {
        symbol: format(index, f"0{code_length}b")
        for index, symbol in enumerate(symbols)
    }

    return original_codes


def build_huffman_tree(grouped_probabilities):
    if not grouped_probabilities:
        raise ValueError("Cannot build a Huffman tree without symbols.")

    heap = []
    insertion_order = count()

    for symbol, probability in grouped_probabilities.items():
        node = {
            "symbol": symbol,
            "left": None,
            "right": None
        }

        heapq.heappush(
            heap,
            (probability, next(insertion_order), node)
        )

    while len(heap) > 1:
        probability1, _, left_node = heapq.heappop(heap)
        probability2, _, right_node = heapq.heappop(heap)

        parent_node = {
            "symbol": None,
            "left": left_node,
            "right": right_node
        }

        heapq.heappush(
            heap,
            (
                probability1 + probability2,
                next(insertion_order),
                parent_node
            )
        )

    return heap[0][2]


def generate_huffman_codes(root):
    huffman_codes = {}

    def traverse(node, current_code):
        if node["left"] is None and node["right"] is None:
            huffman_codes[node["symbol"]] = current_code or "0"
            return

        traverse(node["left"], current_code + "0")
        traverse(node["right"], current_code + "1")

    traverse(root, "")
    return huffman_codes


def build_modified_codes(
    huffman_codes,
    original_codes,
    ordinary_symbols,
    others_symbols
):
    final_codes = {}

    for symbol in ordinary_symbols:
        final_codes[symbol] = huffman_codes[symbol]

    for symbol in others_symbols:
        final_codes[symbol] = (
            huffman_codes[OTHERS_TOKEN] + original_codes[symbol]
        )

    # Reverse the dictionary:
    # code becomes the key, and symbol becomes the value.
    reversed_codes = {
        code: symbol
        for symbol, code in final_codes.items()
    }

    return reversed_codes


def encode_text(text, codes):
    # The codes dictionary is now {code: symbol}.
    # Reverse it locally to get {symbol: code} for encoding.
    symbol_to_code = {
        symbol: code
        for code, symbol in codes.items()
    }

    missing_symbols = set(text) - set(symbol_to_code)

    if missing_symbols:
        raise ValueError(
            f"Missing codes for symbols: {missing_symbols!r}"
        )

    return "".join(
        symbol_to_code[symbol]
        for symbol in text
    )


def modified_huffman_encode(text, min_limit):
    frequencies, probabilities = calculate_probabilities(text)

    (
        ordinary_symbols,
        others_symbols,
        grouped_probabilities
    ) = group_symbols(probabilities, min_limit)

    original_codes = generate_original_codes(frequencies.keys())
    huffman_tree = build_huffman_tree(grouped_probabilities)
    huffman_codes = generate_huffman_codes(huffman_tree)

    final_codes = build_modified_codes(
        huffman_codes,
        original_codes,
        ordinary_symbols,
        others_symbols
    )

    bitstream = encode_text(text, final_codes)

    details = {
        "minimum_limit": min_limit,
        "frequencies": dict(frequencies),
        "probabilities": probabilities,
        "ordinary_symbols": list(ordinary_symbols.keys()),
        "symbols_in_others": list(others_symbols.keys()),
        "original_codes": original_codes,
        "huffman_codes": {
            "Others" if symbol is OTHERS_TOKEN else symbol: code
            for symbol, code in huffman_codes.items()
        },
        "encoded_bit_length": len(bitstream)
    }

    return bitstream, final_codes, details
