import asyncio
import os
from logging import getLogger

import aiofiles
import aiohttp

from util.log_util import error_trace

LOGGER = getLogger(__name__)


class FileDownloader:
    @classmethod
    async def download(self, url, save_dir):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        file_name = url.split("/")[-1]
                        f = await aiofiles.open(os.path.join(save_dir, file_name), mode="wb")
                        await f.write(await resp.read())
                        await f.close()
                        return True
        except Exception as e:
            error_trace(e)
            return False

    @classmethod
    def download_files(self, urls, save_dir):
        os.makedirs(save_dir, exist_ok=True)

        task = [self.download(url, save_dir) for url in urls]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(asyncio.gather(*task))

        if False in results:
            raise Exception("画像ファイルのダウンロードに失敗")


# class FileDownloader:
#     def download_files(self, urls):
#         pass

#     async def download(self, url, session):
#         s = await session.get(url)
#         # await asyncio.sleep(0)  # この行はrequestsバージョンでは必要
#         sentence = await s.text()  # requestsでは.textだが、aiohtttpは.text()
#         return sentence

#     async def text_preprocess(sentence):
#         # 下記は時間がかかる処理を想定
#         a = random.randint(0, 6)
#         print(f"processing for {a} sec")
#         # await asyncio.sleep(a)  # ダウンロード処理時間だけ見たい場合、ここはコメントにする
#         return a

#     async def download_and_preprocess(self, url, session):
#         sentence = await self.download(url, session)
#         return await text_preprocess(sentence)

#     async def do_tasks(urls):
#         async with aiohttp.ClientSession() as session:
#             tasks = [asyncio.create_task(download_and_preprocess(url, session)) for url in urls]
#             results = await asyncio.gather(*tasks)
#             return results

#     def main(self):
#       urls = ["https://www.example.com/domains/reserved", "https://www.example.org/domains/reserved", "https://www.example.edu/domains/reserved"]
#       loop = asyncio.get_event_loop()
#       results = loop.run_until_complete(do_tasks(urls))
#       for r in results:
#         print(f"result:{r}")


# async def do_tasks(urls):
#     async with aiohttp.ClientSession() as session:
#         tasks = [asyncio.create_task(download_and_preprocess(url, session)) for url in urls]
#         results = await asyncio.gather(*tasks)
#         return results


# class FileSplitDownloader:
#     async def get_content_length(self, url):
#         async with aiohttp.ClientSession() as session:
#             async with session.head(url) as request:
#                 return request.content_length

#     def parts_generator(self, size, start=0, part_size=10 * 1024**2):
#         while size - start > part_size:
#             yield start, start + part_size
#             start += part_size
#         yield start, size

#     async def download(self, url, headers, save_path):
#         async with aiohttp.ClientSession(headers=headers) as session:
#             async with session.get(url) as request:
#                 file = await aiofiles.open(save_path, "wb")
#                 await file.write(await request.content.read())

#     async def process(self, url):
#         filename = os.path.basename(urlparse(url).path)
#         tmp_dir = TemporaryDirectory(prefix=filename, dir=os.path.abspath("."))
#         size = await self.get_content_length(url)
#         tasks = []
#         file_parts = []
#         for number, sizes in enumerate(self.parts_generator(size)):
#             part_file_name = os.path.join(tmp_dir.name, f"{filename}.part{number}")
#             file_parts.append(part_file_name)
#             tasks.append(self.download(url, {"Range": f"bytes={sizes[0]}-{sizes[1]}"}, part_file_name))
#         await asyncio.gather(*tasks)
#         with open(filename, "wb") as wfd:
#             for f in file_parts:
#                 with open(f, "rb") as fd:
#                     shutil.copyfileobj(fd, wfd)
