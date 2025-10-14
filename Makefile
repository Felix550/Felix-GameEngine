build:
	nuitka --standalone --onefile --lto=yes --output-dir="output" --include-package=lupa main.py

run:
	python src/main.py -s scripts

clean:
	rmdir /S /Q output