import os


def get_file_list(filedir, type) -> list:
    """获取同一目录下的所有指定类型文件的绝对路径
    Args:
        filedir (str): 文件夹路径
        type (str): 文件类型
    """
    file_list = [
        os.path.join(root, filespath)
        for root, dirs, files in os.walk(filedir)
        for filespath in files
        if str(filespath).endswith(type)
    ]
    return file_list if file_list else []
