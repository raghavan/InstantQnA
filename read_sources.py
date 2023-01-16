import os
from pypdf import PdfReader
from tqdm import tqdm

def dump(include: "list[str]" = None) -> '[str]':
    file_count = sum(len(files) for _, _, files in os.walk("sources")) 
    with tqdm(total=file_count, desc="Reading pdf text content") as pbar:
        for root, _, files in os.walk("sources"):
            for file in files:
                pbar.update(1)
                if include and file not in include or '.gitkeep' in file:
                    continue
                path = os.path.join(root, file)
                with open(os.path.join("ai_generated/dumps", file), "w", encoding="utf-8") as g:
                    pass
                with open(os.path.join("ai_generated/dumps", file), "a", encoding="utf-8") as f:
                    reader = PdfReader(path)
                    for idx, page in enumerate(reader.pages):
                        if idx == 0:
                            continue
                        content = page.extract_text().lower()
                        if "............." in content:
                            continue
                        f.write(content)
    print()
    return include

if __name__ == '__main__':
    dump()