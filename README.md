# RuOtvet
### Library for searching answers to school questions in the big count of services.

# Installation:

###### Download library using pip
```bash
$ pip3 install ruotvet
```

# Usage example:
```python3
from ruotvet import Brainly, get_attachment
import asyncio


async def main():
    questions = await Brainly().get_answers("Корень из 121", count=1)
    for question in questions:
        print(question.answer)
        if question.attachments:
            await get_attachment(attachment=question.attachments[0])
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
# 🤝 Contributing
#### <a href="https://github.com/ruotvet/ruotvet/graphs/contributors" align=center>Feel free to contribute.</a>
