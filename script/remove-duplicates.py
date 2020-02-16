import os


def removeIfExist(path):
    if os.path.exists(path):
        os.remove(path)


def main():
    target_path = './img/imgs.txt'
    out_path = './img/unique.txt'
    removeIfExist(out_path)

    inputfile = open(target_path, 'r')
    outputfile = open(out_path, 'w+')

    ids = set()

    while True:
        line = inputfile.readline().strip()
        if len(line) == 0:
            break

        ids.add(line)

    print(f'Found {len(ids)} unique entries.')
    for path in ids:
        outputfile.write(path+'\n')

    outputfile.close()
    inputfile.close()


if __name__ == '__main__':
    main()
