import os

from collections import Counter


def removeIfExist(path):
    if os.path.exists(path):
        os.remove(path)


def main():
    target_path = './img/imgs.txt'
    out_path = './img/unique.txt'
    frequency_out_path = './img/frequency.txt'
    removeIfExist(out_path)
    removeIfExist(frequency_out_path)

    inputfile = open(target_path, 'r')
    outputfile = open(out_path, 'w+')
    freqoutfile = open(frequency_out_path, 'w+')

    ids = set()
    frequencies = Counter()

    while True:
        line = inputfile.readline().strip()
        if len(line) == 0:
            break

        md5 = line.split(".")[0]
        frequencies[md5] += 1

        ids.add(line)

    print(f'Found {len(ids)} unique entries.')
    for path in ids:
        outputfile.write(path+'\n')

    for md5, freq in frequencies.items():
        freqoutfile.write(f'{md5} {freq}\n')

    outputfile.close()
    inputfile.close()


if __name__ == '__main__':
    main()
