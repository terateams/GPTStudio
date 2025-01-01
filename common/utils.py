import base64
import logging
import jwt
import diskcache as dc
import os
import hashlib



log = logging.getLogger(__name__)


_cache_dir = os.path.join(os.environ.get('DATA_DIR', '/tmp'), "cache")
if not os.path.exists(_cache_dir):
    os.makedirs(_cache_dir)

disk_cache = dc.Cache(_cache_dir)
mem_cache = dc.FanoutCache(
    directory=_cache_dir,  # 磁盘缓存目录
    shards=32,               # 分片数，用于提高并发性能
    size_limit=100 * 10**6           # 内存缓存大小限制，这里设置为100M
)


def md5hash(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

    
def file_hash(filepath: str) -> str:
    with open(filepath, 'rb') as file:
        hash_object = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b''):
            hash_object.update(chunk)
    return hash_object.hexdigest()


def validate_api_key(api_key, api_secret: str) -> bool:
    if api_key:
        try:
            payload = jwt.decode(api_key, api_secret, algorithms=['HS256'])
            uid = payload.get('uid')
            if uid in ["gptservice","teamstools","teamscode"]:
                return True
        except Exception as e:
            return False
    return False

def parse_azureblob_account_info(conn_str: str = None):
    # 获取连接字符串
    # 将连接字符串分割为各个部分
    parts = conn_str.split(";")
    # 提取 AccountName 和 AccountKey
    account_info = {}
    for part in parts:
        if "AccountName=" in part:
            account_info["AccountName"] = part.split("=", 1)[1]
        elif "AccountKey=" in part:
            account_info["AccountKey"] = part.split("=", 1)[1]

    return account_info["AccountName"], account_info["AccountKey"]


def get_global_datadir(subpath: str = None):
    """
    获取全局数据目录。

    Args:
        subpath (str, optional): 子路径。默认为None。

    Returns:
        str: 数据目录路径。
    """
    datadir = os.environ.get("DATA_DIR", "/tmp/teamsgpt")
    if subpath:
        datadir = os.path.join(datadir, subpath)
    if not os.path.exists(datadir):
        os.makedirs(datadir)
    return datadir
    


def is_url(url):
    # 使用正则表达式检查URL是否有效, 不用validators
    return re.match(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", url) is not None




def image_to_base64(image_path):
    """
    Convert an image file to a Base64 encoded string.
    
    :param image_path: Path to the image file
    :return: Base64 encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def base64_to_image(encoded_string, output_path):
    """
    Convert a Base64 encoded string to an image file and save it locally.

    :param encoded_string: Base64 encoded string of the image
    :param output_path: Path where the image file should be saved
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(encoded_string))


def format_latex(text: str) -> str:
    """
    格式化包含LaTeX公式的文本
    将 \frac{a}{b} 这样的文本转换为可显示的LaTeX格式
    """
    # 如果文本中包含LaTeX公式（以\开头的内容），将其用$包围
    if '\\' in text:
        # 替换换行符为HTML换行
        text = text.replace('\\n', '<br>')
        # 分割文本，保留LaTeX公式
        parts = []
        current = []
        in_latex = False
        
        for char in text:
            if char == '\\' and not in_latex:
                if current:
                    parts.append(''.join(current))
                current = [char]
                in_latex = True
            elif in_latex and char in ' .,。，。!?！？':
                current.append(char)
                parts.append(f"${''.join(current)}$")
                current = []
                in_latex = False
            else:
                current.append(char)
                
        if current:
            if in_latex:
                parts.append(f"${''.join(current)}$")
            else:
                parts.append(''.join(current))
                
        return ' '.join(parts)
    return text
