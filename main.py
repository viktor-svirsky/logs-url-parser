from pprint import pprint

from processor import Processor

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    proc = Processor()
    proc.process("logs.csv")
    result = proc.get_result()
    proc.reset()

    pprint(result)
