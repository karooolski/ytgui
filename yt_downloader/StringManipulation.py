class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])


def switch_non_ascii(text):
    return ''.join([i if ord(i) < 128 else 'a' for i in text])