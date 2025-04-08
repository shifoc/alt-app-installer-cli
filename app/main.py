import sys
import argparse
import asyncio

from url_gen import get_app_info
from download import download
from install import install

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

parser = argparse.ArgumentParser(description="Alt App Installer CLI Help")
parser.add_argument("input", help="Microsoft Store URL or Product ID")
parser.add_argument(
    "-d",
    "--download_only",
    help="Download only, do not install",
    action="store_true",
)
parser.add_argument(
    "-i",
    "--ignore_ver",
    help="Ignore version of dependencies",
    action="store_true",
)
parser.add_argument(
    "-a",
    "--all_dependencies",
    help="Include all dependencies",
    action="store_true",
)
parser.add_argument(
    "-v",
    "--info_only",
    help="Retrieve and display app info only",
    action="store_true",
)
parser.add_argument(
    "-k",
    "--insecure",
    help="Disable SSL verification",
    action="store_true",
)

args = parser.parse_args()
verify_ssl = not args.insecure

if args.info_only:
    print("Fetching app info...")
    info = asyncio.run(get_app_info(args.input, verify_ssl))
    print(f"Name        : {info['name']}")
    print(f"Version     : {info['version']}")
    print(f"Publisher   : {info['publisher']}")
    print(f"Last Update : {info['last_update']}")
    print(f"Product ID  : {info['product_id']}")
    exit(0)
print("Downloading Packages...")
data = download(args.input, args.ignore_ver, args.all_dependencies, verify_ssl)
if not args.download_only:
    print("Installing Packages...")
    install(*data)