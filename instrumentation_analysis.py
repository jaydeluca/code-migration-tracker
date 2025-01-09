from datetime import datetime
from typing import List, Set
import pandas as pd

from github_client import GithubClient


class Instrumentation:
    def __init__(self, name: str, has_javaagent: bool = False,
                 has_library: bool = False, parent: str = None):
        self.name = name
        self.has_javaagent = has_javaagent
        self.has_library = has_library
        self.parent = parent


def analyze_instrumentation(file_list: List[str]) -> List[Instrumentation]:
    instrumentations = {}
    for i in file_list:
        parts = i.split("/")
        inst_name = parts[0]
        parent = None
        if len(parts) > 2:
            inst_name = parts[len(parts) - 2]
            parent = i.split(inst_name)[0].rstrip("/")
        inst = instrumentations.get(inst_name, Instrumentation(inst_name))
        if i.endswith("/javaagent"):
            inst.has_javaagent = True
        elif i.endswith("/library"):
            inst.has_library = True

        inst.parent = parent
        instrumentations[inst_name] = inst

    items = list(instrumentations.values())
    return items


def parse_readme(file_list: List[str]) -> (Set[str], Set[str]):
    javaagent_has_readme = set()
    library_has_readme = set()

    for i in file_list:
        parts = i.split("/")
        if i.lower().endswith("javaagent/readme.md"):
            javaagent_has_readme.add(parts[len(parts) - 3])
        elif i.lower().endswith("library/readme.md"):
            library_has_readme.add(parts[len(parts) - 3])

    return javaagent_has_readme, library_has_readme


def main():
    repo = "open-telemetry/opentelemetry-java-instrumentation"
    client = GithubClient()
    today = (datetime.now().date() + pd.Timedelta(days=1)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")

    commit = client.get_most_recent_commit(repo, today, "main")
    repo_files = client.get_repository_at_commit(
        repository=repo,
        commit_sha=commit
    )

    instrumentations = []
    readmes = []

    for i in repo_files["tree"]:

        if i["path"].lower().endswith("readme.md"):
            readmes.append(i["path"].replace("instrumentation/", ""))

        if i["path"].startswith("instrumentation/") \
                and i["type"] == "tree" \
                and (i["path"].endswith("/javaagent") or i["path"].endswith("/library")) \
                and "/io/opentelemetry/javaagent" not in i["path"] \
                and "-common/" not in i["path"]:

            instrumentations.append(i["path"].replace("instrumentation/", ""))

    inst_list = analyze_instrumentation(instrumentations)
    javaagent_has_readme, library_has_readme = parse_readme(readmes)
    library: List[Instrumentation] = []
    javaagent: List[Instrumentation] = []

    no_javaagent = []

    output = ""
    for i in inst_list:
        output += f"{i.name}:\n"
        if i.has_javaagent:
            output += " javaagent\n"
            javaagent.append(i)
        else:
            no_javaagent.append(i)
        if i.has_library:
            output += " library\n"
            library.append(i)

    javaagent_count = len(javaagent)
    library_count = len(library)

    print(f"{len(inst_list)} instrumentation items")
    print("\n")
    print(f"{javaagent_count} javaagent instrumentations ({int(javaagent_count / len(inst_list) * 100)}%)")
    print(f"Readmes: {len(javaagent_has_readme)}\n\n")

    print(f"{library_count} library instrumentations ({int(library_count / len(inst_list) * 100)}%)")
    print(f"Readmes: {len(library_has_readme)}")

    print("\nLibraries:\n")
    for i in library:
        full_inst_name = f"{i.parent}/{i.name}" if i.parent else i.name
        link = f"https://github.com/open-telemetry/opentelemetry-java-instrumentation/tree/main/instrumentation/{full_inst_name}/library"
        print(f"{'- [x]' if i.name in library_has_readme else '- [ ]'} [{i.name}]({link})")


if __name__ == '__main__':
    main()
