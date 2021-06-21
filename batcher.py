from os import path
import sys


def readWord(reader):
    return reader.readline().rstrip()


def get_known_words():
    known_words_file_name = "known_words.txt"
    known_words = set()

    if path.isfile(known_words_file_name):
        with open(known_words_file_name, "r") as reader:
            for _ in range(2):
                next(reader)
            word = readWord(reader)
            while word != "":
                known_words.add(word)
                word = readWord(reader)
    else:
        known_words_file = open(known_words_file_name, "w")
        known_words_file.write("0\n\n")
        known_words_file.close()

    return known_words


def save_known_words(known_words):
    known_words_file_name = "known_words.txt"

    with open(known_words_file_name, "w") as writer:
        writer.write(str(len(known_words)) + "\n\n")
        writer.writelines(map(lambda s: s + "\n", known_words))


def write_batch(writer, batch, number, character_count):
    writer.write(f"Batch {number}\n")
    writer.write(f"{character_count} characters\n")
    writer.write(f"{len(batch)} words\n")
    writer.write(", ".join(batch))
    writer.write("\n\n")


def batch(input_file_name, output_file_name, character_limit, words_limit):
    known_words = get_known_words()
    number_of_words_skipped = 0
    number_of_batches = 0
    batch = []
    batch_character_count = 0

    with open(input_file_name, "r") as reader, open(output_file_name, "w") as writer:
        for _ in range(2):
            next(reader)
        word = readWord(reader)
        while word != "":
            if word not in known_words:
                known_words.add(word)
                if (
                    batch_character_count + len(word) < character_limit
                    and len(batch) < words_limit
                ):
                    batch.append(word)
                    batch_character_count += len(word) + (2 if len(batch) > 1 else 0)
                else:
                    write_batch(
                        writer, batch, number_of_batches + 1, batch_character_count
                    )
                    number_of_batches += 1
                    batch = []
                    batch_character_count = 0
            else:
                number_of_words_skipped += 1
            word = readWord(reader)
        write_batch(writer, batch, number_of_batches + 1, batch_character_count)

    save_known_words(known_words)
    
    return output_file_name


def main():
    batch(
        sys.argv[1],
        sys.argv[2] if (len(sys.argv) >= 3) else sys.argv[1][:-4] + "_batcher_out.txt",
        sys.argv[3] if (len(sys.argv) >= 4) else 4950,
        sys.argv[4] if (len(sys.argv) >= 5) else 400,
    )


if __name__ == "__main__":
    main()
