#!/usr/bin/env python3
# Scans a directory recursively and creates symlinks in another directory
# to all the markdown files it found.

import os
import yaml
import shutil
import fnmatch
import copy
import subprocess
from collections import defaultdict

class ScanMarkDown(object):

    build_directory = ""

    def __init__(self):
        self.parse_config()
        self.setup_build_directory()
        self.scan()
        self.run_mkdocs()

    def parse_config(self):
        doc = None
        with open("config.yaml", 'r') as f:
            try:
                doc = yaml.load(f)
            except yaml.YAMLError as err:
                print(err)
                exit
            self.build_directory = doc['build_dir']

    def setup_build_directory(self):
        build_path = os.environ.get('DOC_BUILD_DIR', self.build_directory)
        try:
            shutil.rmtree(os.path.join(build_path, "docs"))
        except FileNotFoundError:
            pass
        try:
            shutil.copytree("docs", os.path.join(build_path, "docs"))
        except FileExistsError:
            print ("Unable to copy documentation files to build directory")
            exit()


    def scan(self):
        matches = []
        out_dict = defaultdict(set)

        # Grab environment overrides

        self.workdir = os.path.abspath(os.curdir)
        self.topdir = self.workdir.rstrip(os.path.basename(self.workdir))

        os.chdir("../")
        for root, dirnames, filenames in os.walk("."):
            for filename in fnmatch.filter(filenames, '*.md'):
                matches.append(os.path.join(root, filename))
                for match in matches:
                    name = os.path.basename(match)
                    # If the name is index.md verify that a docs directory is above
                    # If this is the case then format a nice line for the output
                    parent_dir = ""
                    title_name = ""
                    # Skip the documentation directory itself
                    if "docs/docs" in os.path.dirname(match):
                        continue
                    if os.path.dirname(match).split('/')[-1] == "docs":
                        name = os.path.dirname(match).split('/')[-2].replace('_', ' ')
                        parent_dir = os.path.dirname(match).split('/')[-3]
                        if parent_dir == "docs":
                            continue
                        if parent_dir == ".":
                            parent_dir = name
                        out_dict[parent_dir].add((name, match))
                    else:
                        # This is a file at a top level, outside of a docs directory.
                        # This makes the paths index slightly different
                        name = os.path.dirname(match).split('/')[-1].replace('_', ' ')
                        if name == ".":
                            # A markdown file created at the top of the repo will be put into the "SDA" menu
                            parent_dir = "SDA"
                        else:
                            parent_dir = os.path.dirname(match).split('/')[-2]
                        if parent_dir == "docs":
                            continue
                        out_dict[parent_dir].add((name, match))

        self.create_dir_structure(out_dict)
        shutil.copy(os.path.join(self.workdir, "mkdocs.template"), os.path.join(self.build_directory, "mkdocs.yml"))
        if len(out_dict.items()) > 0:
            with open(os.path.join(self.build_directory, 'mkdocs.yml'), 'a') as f:
                for key, val in sorted(out_dict.items()):
                    # Capitalize only first letter, to leave abbreviations alone
                    print("- " + self.first_char_to_upper(key) + ":", file=f)
                    for v in sorted(val):
                        print (v)
                        output_name = os.path.basename(v[1]).rstrip('.md').replace("_", " ")
                        # If the directory name is the same as the top dir, don't add it again.
                        directory_name = ""
                        # A top level markdown file needs to be handled a bit differently to not have a "." as a directory name.
                        # This is the reason for the "SDA" check.
                        if v[0] == key or key == "SDA":
                            directory_name = ""
                        else:
                            directory_name = self.first_char_to_upper(v[0]) + ' - '
                        print("    - '" + directory_name + output_name.title() + "': '" + os.path.normpath(os.path.join("docs", (v[1]))) + "'", file=f)

    def first_char_to_upper(self, key):
        first_char = key[0]
        if first_char.isalpha():
            first_char = first_char.upper()
            rest = key[1:]
            return first_char + rest
        return key

    def create_dir_structure(self, entries):
        set_entries = copy.copy(entries)
        os.chdir(os.path.join(self.build_directory, "docs"))
        for key, val in set_entries.items():
            for v in val:
                try:
                    os.makedirs(os.path.join("docs", os.path.dirname(v[1])))
                except FileExistsError:
                    pass
                try:
                    target = os.path.abspath(os.path.join("docs", v[1]))
                    source = os.path.abspath(os.path.join(os.path.dirname(self.workdir), v[1]))
                    shutil.copy(source, target)
                except FileExistsError:
                    pass

    def run_mkdocs(self):
        os.chdir("..")
        subprocess.call(["mkdocs", "build", "--clean"])


if __name__ == "__main__":
    m = ScanMarkDown()
