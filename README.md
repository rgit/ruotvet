# RuOtvet
### Library for searching answers to school questions in the big count of services.

# Installation:

###### Download library using pip
```bash
$ pip3 install ruotvet
```

# Usage example:
```python3
from ruotvet import Znanija
import asyncio


async def main():
    for obj in (await Znanija().get_answers("Корень из 121", count=1))[0]:
        print(obj)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
# 🤝 Contributing
#### <a href="https://github.com/ruotvet/ruotvet/graphs/contributors" align=center>Feel free to contribute.</a>
