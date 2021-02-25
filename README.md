<h1>RuOtvet</h1>
<h4>Library for searching answers to school questions in the big count of services.</h4>


<h2>Installation:</h2>
<h6>Download library using pip</h6>

```bash
$ pip3 install ruotvet -U
```


<h2>Usage examples:</h2>

<h3>Query with attachment saving example:</h3> 

```python3
from ruotvet.utils import get_attachment
from ruotvet import Brainly
import asyncio


async def main():
    questions = await Brainly().get_answers("Корень из 121", count=1)
    for question in questions:
        print("Answer: ", question.answer)
        if question.attachments:
            print("Answer attachment: ", await get_attachment(attachment=question.attachments[0]))
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

<br>

<h3>Image OCR example:</h3>

<p>Before using OCR you need to install tesseract and your language data for it:</p>
<p>In macOS simply install it using brew:</p>

```bash
$ brew install tesseract
$ brew install tesseract-lang
```

<p>In unix-like you should do it like this:</p>

```bash
$ sudo apt-get install tesseract-ocr
$ sudo apt-get install tesseract-ocr-all
```

<p>For using OCR in Windows, follow this <a href="https://github.com/UB-Mannheim/tesseract/wiki">instruction</a>.</p>





```python3
from ruotvet.utils import OCR
from ruotvet import Brainly
import asyncio


async def main():
    query = OCR().recognize("image.png")["text"]
    questions = await Brainly().get_answers(query, count=1)
    for question in questions:
        print("Answer: ", question.answer)
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


<h2>License</h2>
<p>The library is under the GNU LGPLv3 license.</p>
<p>
    BE AWARE THAT THE AUTHORS ARE UNDER NO CIRCUMSTANCES RESPONSIBLE FOR CONSEQUENCES OF USE AND 
    ANY INTERACTION WITH THE LIBRARY. NOT LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
    IN THE SOFTWARE. THE CODE IS PROVIDED FOR EDUCATION PURPOSES ONLY.
</p>
<p>
    Read the <a href="https://github.com/rgit/ruotvet/blob/master/LICENSE">LICENSE</a> for more information.
</p>


<h2>Contributing</h2>

<a href="https://github.com/rgit/ruotvet/graphs/contributors">Feel free to contribute.</a>
