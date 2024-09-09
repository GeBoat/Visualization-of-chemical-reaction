import os
import shutil

def organize_files(source_folder):

    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    for file in files:
        # 验证文件名是否符合 'ben_id_benX_' 格式
        if 'ben_id_ben' not in file:
            continue

        try:
            # 解析文件名以获取ben的索引
            ben_index_str = file.split('_')[2][3:]
            ben_index = int(ben_index_str)

            # 创建目标文件夹路径
            target_folder = os.path.join(source_folder, f'ben{ben_index}')
            os.makedirs(target_folder, exist_ok=True)

            # 分别处理结果文件和bonds文件的命名
            if '_result.txt' in file:
                new_file_name = 'result.txt'
            elif '_bonds' in file:
                bonds_index_str = file.split('_')[3][5:-4]
                bonds_index = int(bonds_index_str)
                new_file_name = f'bonds{bonds_index}.txt'
            else:
                continue  # 跳过不符合这两种格式的文件

            # 移动文件到目标文件夹并修改文件名为新的名称
            target_file = os.path.join(target_folder, new_file_name)
            shutil.move(os.path.join(source_folder, file), target_file)
        except ValueError:
            print(f"无法从文件名'{file}'中提取有效索引，跳过该文件。")

