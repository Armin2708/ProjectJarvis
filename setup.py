import os
import subprocess
import sys


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


def main():
    with open('requirements.txt', 'r') as f:
        packages = f.readlines()

    for package in packages:
        install(package.strip())


if __name__ == "__main__":
    main()