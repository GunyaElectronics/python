import os

def fix_ddf_paths():
    for filename in os.listdir('.'):
        if filename.lower().endswith('.ddf'):
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            modified = False
            with open(filename, 'w', encoding='utf-8') as f:
                for line in lines:
                    if 'File = $TOOLKIT_DIR$\\config\\ddf\\' in line:
                        line = line.replace('File = $TOOLKIT_DIR$\\config\\ddf\\', 'File = ')
                        modified = True
                    f.write(line)

            if modified:
                print(f"[✓] Modified: {filename}")
            else:
                print(f"[ ] Unchanged: {filename}")

if __name__ == "__main__":
    fix_ddf_paths()
