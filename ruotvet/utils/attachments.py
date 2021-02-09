from string import ascii_uppercase, ascii_letters, digits
from ..http import AIOHTTPClient
from ..types import Attachment
from random import choice
import aiofiles


async def get_attachment(attachment: Attachment) -> Attachment:
    filename = "".join(choice(ascii_uppercase + ascii_letters + digits) for _ in range(8)) + ".png"
    client = AIOHTTPClient()
    async with aiofiles.open(filename, mode="wb") as media:
        content = await client.request_content("GET", attachment.url)
        await media.write(content)
        await media.close()
    await client.close()
    return attachment.copy(update={"path": filename})
