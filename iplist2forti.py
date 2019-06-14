#! /usr/bin/python

import argparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='WireShark stats to FortiGate.')

    p.set_defaults(
        delimiter='\t',
        skip_repeats=True
    )

    addarg = p.add_argument

    addarg('-i', '--in-file', dest='in_file', required=True,
           help='input file')
    addarg('-o', '--out-file', dest='out_file', required=True,
           help='output file')
    addarg('-d', '--delimiter', dest='delimiter',
           help='delimiter')
    addarg("--skip-repeats", type=bool, dest='skip_repeats',
           help='Skip the same URLs')

    return p.parse_args()


def main() -> None:
    args = parse_args()

    with open(args.in_file) as file:
        lines = file.readlines()

    urls = [line[1].strip('\n') for line in map(lambda x: x.split(args.delimiter), lines)]

    if args.skip_repeats:
        without_subdomain_urls = set(urls)

    with open(args.out_file, 'w') as file:
        file.write("config firewall proxy-address\n")
        for url in without_subdomain_urls:
            file.write("    edit \"%s\"\n" % url)
            file.write("        set host \"all\"\n")
            file.write("        set path \"%s\"\n" % url)
            file.write("    next\n")
        file.write("end")


if __name__ == '__main__':
    main()
