import pyqrcode as qr
import base64
import io


async def gererated_qr_code(link):
    """Функция генерации qr-кода и приведение в формат base64 для отправки в json"""
    qr_code = qr.create(link)
    stream = io.BytesIO()
    qr_code.png(stream, scale=6)
    qr_code_str = base64.b64encode(stream.getvalue()).decode("utf-8")
    return qr_code_str
