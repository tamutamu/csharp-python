import mmap
import time

WORD_SIZE = 10
MMAP_FILE_NAME = "MAP_TEST"

mm = mmap.mmap(0, 0, MMAP_FILE_NAME)

def mmapReadString(adr:int):
        """指定のアドレスの値を読み込む(Shortデータ)

        Args:
            adr : Shared memory address
        """    
        try:
            mm.seek(adr*WORD_SIZE)
            bytes = mm.read(WORD_SIZE)
            val = str.from_bytes(bytes, 'little',signed=True)
            mm.seek(0)
            return val
        except Exception as e:
            return None

if __name__ == "__main__":
    mm.seek(0)
    print(mm.readline().decode('utf_8_sig'))
