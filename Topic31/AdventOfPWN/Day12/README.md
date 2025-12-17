# Day 12


```py
from pathlib import Path
import angr

files = [p for p in Path("naughty-or-nice/").iterdir() if p.is_file()]
current_files = [p.name for p in Path("seeds/").iterdir() if p.is_file()]



for file in files:
    if file.name not in current_files:
        p = angr.Project(f'{file}', auto_load_libs=False)
        state = p.factory.entry_state()
        sm = p.factory.simulation_manager(state)
        # sm = p.factory.simulation_manager(state)
        sm.explore(find=lambda s: b'Correct' in s.posix.dumps(1), avoid=lambda s: b'Wrong' in s.posix.dumps(1))
        input_0 = sm.found[0].posix.dumps(0).strip(b'\0')

        with open(f"./seeds/{file.name}", "wb") as f:
            f.write(input_0)
        
    else:
        print("there")
        continue
```
