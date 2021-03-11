from string import ascii_uppercase, ascii_letters, digits
from ..types import Attachment, File
from ..http import AIOHTTPClient
from random import choice
import aiofiles


async def get_attachment(attachment: Attachment, path: str = None) -> Attachment:
    filename = "".join(choice(ascii_uppercase + ascii_letters + digits) for _ in range(8)) + ".png"
    path = f"{path}/{filename}" if path else filename
    client = AIOHTTPClient()
    async with aiofiles.open(path, mode="wb") as media:
        content = await client.request_content("GET", attachment.url)
        await media.write(content)
        await media.close()
    await client.close()
    return attachment.copy(update={"file": File(filename=filename, path=path, format="png")})
