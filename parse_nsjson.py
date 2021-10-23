import ipaddress
import json
import os
import re
from collections import defaultdict


ignores = [
    "onepassword",
    "shadowrocket",
    "telegraph",
    "firefox",

    "com_apple",
    "com_google",
    "com_facebook",
]
IgnoreRE = re.compile("(%s)+" % "|".join(ignores), re.IGNORECASE)


def sort_out():
    bucket = defaultdict(set)

    for file in os.listdir("."):
        if file.endswith(".ndjson") and os.path.isfile(file):
            with open(file, "r") as rf:
                assets = rf.read().split("\n")

            for asset in assets:
                if not asset:
                    continue

                asset = json.loads(asset)
                if "domain" in asset:
                    try:
                        ipaddress.ip_address(asset["domain"])
                    except ValueError:
                        bucket[asset["bundleID"]].add(asset["domain"])

    for app_name, domains in bucket.items():
        app_name = app_name.replace(".", "_")
        if re.search(IgnoreRE, app_name):
            continue

        if not os.path.exists(f"ios/{app_name}.txt"):
            with open(f"ios/{app_name}.txt", "w", encoding="utf8") as wf:
                wf.write("\n".join(sorted(domains)))
        else:
            with open(f"ios/{app_name}.txt", "r", encoding="utf8") as rf:
                lines = rf.read().split("\n")
            with open(f"ios/{app_name}.txt", "w", encoding="utf8") as wf:
                wf.write("\n".join(sorted(domains.union(lines))))


if __name__ == '__main__':
    sort_out()
