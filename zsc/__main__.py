import zsc.compiler as compiler
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="zsc",
        description=f'Python to ZScript transpiler ({compiler.VERSION})'
    )
    parser.add_argument("input", help="path to python source file")
    parser.add_argument(
        "--output", help="optional output file (otherwise, uses the same name as the input file with .txt extension)")
    parser.add_argument(
        "--show", help="if true, print the transpiled file to stdout", action='store_true')

    args = parser.parse_args()
    output, result = compiler.compile(args.input, out_filename=args.output or '')

    if args.show:
        print(result)
    else:
        print(output)
