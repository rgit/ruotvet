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

znanija = Znanija()
for obj in await znanija.get_answer("Корень из 212", count=1):
    print(obj)
```
# 🤝 Contributing
#### <a href="https://github.com/ruotvet/ruotvet/graphs/contributors" align=center>Feel free to contribute.</a>
