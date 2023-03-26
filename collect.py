import os


def collect():
    bucket = []

    for file in os.listdir("ios"):
        fp = os.path.join("ios", file)
        if file.endswith(".txt") and os.path.isfile(fp):
            with open(fp, "r") as rf:
                lines = rf.read().split("\n")

                bucket.extend(lines)

    with open("collects.txt", "w") as wf:
        wf.write("\n".join(sorted(set(bucket))))


if __name__ == '__main__':
    collect()
