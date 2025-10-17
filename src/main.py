import os
import sys
import subprocess
import argparse
import nuitka

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

parser = argparse.ArgumentParser(description="Felix Engine")
parser.add_argument("--compile", action="store_true", help="Compila")
parser.add_argument("-o", "--output", default="output", help="Cartella di destinazione della compilazione")
parser.add_argument("-s", "--source", default="scripts", help="Cartella di avvio entry point principale")
parser.add_argument("-e", "--entry", default="main.lua", help="File di avvio entry point principale")
parser.add_argument("-a", "--assets", default="assets", help="Cartella di assets principale")
args = parser.parse_args()

SCRIPTS_PATH = args.source
ENTRY_SCRIPT = os.path.join(SCRIPTS_PATH,args.entry)
ASSETSFOLDER = args.assets

def compile_with_nuitka(output_dir):
    print("[INFO] Compilazione con Nuitka in corso...")

    os.makedirs(output_dir, exist_ok=True)

    nuitka_cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--lto=yes",
        "--include-package=lupa",
        "--include-data-dir=scripts=scripts",
        f"--output-dir={output_dir}",
        os.path.basename(__file__)
    ]

    try:
        subprocess.check_call(nuitka_cmd)
        print(f"[OK] Compilato! In: {os.path.abspath(output_dir)}")
    except subprocess.CalledProcessError as e:
        print(f"[ERRORE] OPPSIE!: {e}")
        sys.exit(1)

if args.compile:
    compile_with_nuitka(args.output)
    sys.exit(0)

import Excec

if not os.path.exists(ENTRY_SCRIPT):
    print(f"Script main mancante: {ENTRY_SCRIPT}")
    sys.exit(1)
    
if not os.path.exists(ASSETSFOLDER):
    print(f"Cartella assets mancante: {ASSETSFOLDER}")
    sys.exit(1)

with open(ENTRY_SCRIPT, "r", encoding="utf-8") as f:
    code = f.read()

excecuter = Excec.excecuter(os.path.abspath(ASSETSFOLDER), os.path.abspath(ENTRY_SCRIPT))
excecuter.run(code)
