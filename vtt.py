import sys
import re


def parse_vtt(input_file_name, output_file_name):
    all_words = []
    seen_words = set()

    with open(input_file_name, "r") as reader:
        next(reader)
        line = reader.readline()
        while line != "":
            if not re.match(r"(^\d*$|^\s*$|.*-->.*|^NOTE .*)", line):
                parts = line.split()
                words = map(lambda s: re.sub(r"<[^>]*>|[^\w]", "", s), parts)
                for word in words:
                    if word != "" and word not in seen_words:
                        seen_words.add(word)
                        all_words.append(word)
            line = reader.readline()

    with open(output_file_name, "w") as writer:
        writer.write(str(len(all_words)) + "\n\n")
        writer.writelines(map(lambda s: s + "\n", all_words))

    return output_file_name


def main():
    output_file_name = parse_vtt(
        sys.argv[1],
        sys.argv[2] if (len(sys.argv) >= 3) else sys.argv[1][:-4] + "_vtt_out.txt",
    )
    print(output_file_name)


if __name__ == "__main__":
    main()
