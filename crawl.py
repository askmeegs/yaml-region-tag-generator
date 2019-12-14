import yaml
from pathlib import Path
import os
import git
import time
import shutil
import subprocess

from time import gmtime, strftime


google_license = """
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

all_results = {}
repo = None

def generate_region_tag(product, twoup, oneup, snippet):
    if 'kind' not in snippet:
        print("**** snippet " + snippet + "is invalid")
        return ""
    resource_type = snippet['kind'].lower()
    name = snippet['metadata']['name'].lower()
    tag = "{}_{}_{}_{}_{}".format(product, twoup, oneup, resource_type, name)
    tag = tag.replace("-", "_")
    return tag


def process_file(product, twoup, oneup, fn):
    global all_results
    with open(fn) as file:
        results = {}
        documents = yaml.load_all(file)
        for snippet in documents:
            if snippet is None:
                continue
            tag = generate_region_tag(product, twoup, oneup, snippet)
            # handle duplicates.
            if tag in all_results:
                print("⭐️ tag {} already in all_results, adding a #". format(tag))
                x = 2
                numbered_tag = tag + str(x)
                while numbered_tag in all_results:
                    print("tag {} already in all_results, adding a #". format(numbered_tag))
                    x = x + 1
                    numbered_tag = tag + str(x)
                print("adding numbered tag: {} to all_results \n".format(numbered_tag))
                results[numbered_tag] = snippet
                all_results[numbered_tag] = snippet
            else:
                results[tag] = snippet
                all_results[tag] = snippet

    file.close()
    # write new YAML file with google license, START and END
    with open(fn, 'w') as output:
        output.write(google_license + "\n")
        for tag, snippet in results.items():
            start = "# [START {}]".format(tag)
            end = "# [END {}]".format(tag)
            output.write(start + "\n")
            yaml.dump(snippet, output)
            output.write(end + "\n")
            output.write("---\n")
    output.close()

def clone_repo(id_rsa, known_hosts, github_repository, branch, local_path):
    global repo

    # prep to clone
    my_env = os.environ.copy()
    my_env["SSH_PRIVATE_KEY"] = id_rsa
    my_env["KNOWN_HOSTS"] = known_hosts
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cmd = '{}/clone_prep.sh'.format(dir_path)
    a = subprocess.run(cmd, stdout=subprocess.PIPE, env=my_env)
    print(a.stdout.decode('utf-8'))

    # clone
    repo_clone_url = 'git@github.com:{}.git'.format(github_repository)
    repo = git.Repo.clone_from(repo_clone_url, local_path)
    # refs = str(branch)
    # spl = refs.split("/")
    # b = spl[-1]
    repo.git.checkout(branch)

def push_to_repo(local_path, branch):
    global repo
    dt = strftime("%m/%d/%Y %h:%M:%S", gmtime())
    dir_path = os.path.dirname(os.path.realpath(__file__))

    my_env = os.environ.copy()
    my_env["LOCAL_PATH"] = local_path
    my_env["BRANCH"] = branch
    my_env["COMMIT_MESSAGE"] = '[bot] generate YAML region tags {}'.format(dt)
    cmd = '{}/push.sh'.format(dir_path)

    # use script to push to github, as yamlbot
    # (no error catching / logs when doing this in python)
    a = subprocess.run(cmd, stdout=subprocess.PIPE, env=my_env)
    print(a.stdout.decode('utf-8'))


def log_results():
    global all_results
    print("✅ success: total resources processed: {}".format(len(all_results.keys())))


if __name__ == "__main__":
    id_rsa = os.environ['ID_RSA']
    if id_rsa == "":
        print("Error: ID_RSA env variable must be set")
        exit(1)

    known_hosts = os.environ['KNOWN_HOSTS']
    if known_hosts == "":
        print("Error: KNOWN_HOSTS env variable must be set")
        exit(1)

    product = os.environ['PRODUCT']
    if product == "":
        print("Error: PRODUCT env variable must be set")
        exit(1)


    github_repo_name = os.environ['GITHUB_REPOSITORY']
    if github_repo_name == "":
        print("Error: GITHUB_REPOSITORY env variable must be set.")
        exit(1)

    branch = os.environ['GITHUB_REF']
    if branch == "":
        print("Error: GITHUB_REF env variable must be set.")
        exit(1)

    # clone repo
    local_path = "/tmp/{}".format(github_repo_name)
    shutil.rmtree(local_path, ignore_errors=True)
    clone_repo(id_rsa, known_hosts, github_repo_name, branch, local_path)

    # prepare to process snippets
    path = Path(local_path)

    for p in path.rglob("*.yaml"):
        filename = p.name
        fullparent = str(p.parent)
        fn = fullparent +  "/" + filename
        print("processing: {}".format(fn))
        spl = fullparent.split("/")
        oneup = spl[-1]
        twoup = spl[-2]
        process_file(product, twoup, oneup, fn)

    push_to_repo(local_path, branch)
    log_results()