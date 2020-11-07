#!/usr/bin/env python

import sys, os, json, requests, configparser, colorama
from termcolor import colored
from datetime import datetime

colorama.init()

def makeSettingsFile():
    config = configparser.ConfigParser()
    config.add_section('settings')
    
    while True:
        path = input(colored("Input a base path where your projects will be created > ", "cyan"))

        if os.path.isdir(path):
            config['settings']['base_path'] = path
            break

        print(colored("Invalid path\n", "red"))

    while True:
        editor = input(colored("Input your primary code editor > ", "cyan"))

        if editor.lower() in ["visual studio code", "vs code", "vscode"]:
            config['settings']['code_editor'] = "vscode"
            break
        elif editor.lower() in ["vim", "vi"]:
            config['settings']['code_editor'] = "vim"
            break
        
        print(colored("Invalid code editor\n", "red"))

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

def fetchSettings():
    if not os.path.isfile('settings.ini'):
        makeSettingsFile()

        print("\n")

    config = configparser.ConfigParser()
    config.read('settings.ini')
    base_path = config['settings']['base_path']
    code_editor = config['settings']['code_editor']

    return base_path, code_editor

def getLicense():
    while True:
        license_ = input(colored("Input the license you want to use > ", "cyan"))

        if "mit" in license_.lower():
            return "mit"
        elif "boost" in license_.lower() or "bsl" in license_.lower():
            return "bsl-1.0"
        elif "apache" in license_.lower():
            return "apache-2.0"
        elif "mozilla" in license_.lower() or "mpl" in license_.lower():
            return "mpl-2.0"
        elif "lgpl" in license_.lower():
            return "lgpl-3.0"
        elif "agpl" in license_.lower():
            return "agpl-3.0"
        elif "gpl" in license_.lower():
            return "gpl-3.0"
        elif license_.lower() == "unilicense":
            return "unilicense"
        elif license_.lower() in ["nolicense", "no license", "none"]:
            return "no license"

        print(colored("Invalid license\n", "red"))

def createFiles(project_name, code_license):
    files = ""
    files += f"echo '# {project_name}' > README.md"
    
    if code_license != "no license":
        license_page = requests.get(f'https://api.github.com/licenses/{code_license}')
        license_body = json.loads(license_page.text)["body"].replace("[year]", str(datetime.now().year))

        files += f"&& echo '{license_body}' > LICENSE"

    return files

def openCodeEditor(code_editor):
    if code_editor == "vscode":
        return "code ."
    elif code_editor == "vim":
        return "vi README.md"
    return ""

def main():
    if len(sys.argv) == 1:
        base_path, code_editor = fetchSettings()
        project_name = input(colored("Input a name your project > ", "cyan"))
        code_license = getLicense()   

        os.system(f'cd {base_path} && mkdir {project_name} && cd {project_name} && {createFiles(project_name, code_license)} && {openCodeEditor(code_editor)}')
    elif sys.argv[1] == "-settings":
        makeSettingsFile()

main()
