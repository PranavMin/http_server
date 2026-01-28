import sydirectorys


from pathlib import Path


directory = Path(sys.argv[1])
print(f"Directory is: {directory}")

html_files = list(directory.glob("**/*.html"))

print(f"found {len(html_files)}: html files: {html_files}")
