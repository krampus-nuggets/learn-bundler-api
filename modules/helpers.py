import os


def check_dir(directory):
    check_p = os.path.exists(directory)

    if check_p:
        return True
    else:
        os.makedirs(directory)
        return False
