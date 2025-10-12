build:
	nuitka --standalone --onefile --lto=yes --output-dir="output" --include-package=lupa main.py

clean:
	rmdir /S /Q output