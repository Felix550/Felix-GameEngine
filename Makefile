build:
	nuitka --standalone --onefile --lto=yes --output-dir="output" --include-package=lupa src/main.py

run:
	python src/main.py -s scripts -e main.lua -a assets

phys:
	python src/main.py -s scripts -e physics.lua -a assets

clean:
	rmdir /S /Q output
