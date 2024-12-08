# 版权声明：本代码遵循MIT许可证。同时，使用者在使用、修改和分发本代码时，应保留所有原始注释。
# 作者：黄荣彬
# Email：2607037721@qq.com
import xml.etree.ElementTree as ET
import os
import glob
import re
from collections import Counter, defaultdict
import pandas as pd


def remove_xml_declaration(content):
    # 使用正则表达式移除XML声明
    return re.sub(r'^<\?xml[^>]+\?>', '', content, count=1)


def parse_settings(settings_str):
    """解析 settings 属性，提取 -apMac 和 -apSN 的值"""
    settings = {}
    if settings_str:
        # 使用正则表达式匹配键值对
        pattern = re.compile(r'-([a-zA-Z]+)\s+([^\s]+)')
        matches = pattern.findall(settings_str)
        for key, value in matches:
            settings[key] = value.strip('"')
    return settings


def format_mac_address(mac_address):
    """将 MAC 地址格式化为 00E0-FC8D-6370 格式"""
    if not mac_address:
        return 'N/A'

    # 移除所有非字母数字字符（如冒号、破折号等）
    mac_clean = re.sub(r'[^0-9A-Fa-f]', '', mac_address)

    # 确保 MAC 地址长度为 12 个字符
    if len(mac_clean) != 12:
        return 'Invalid MAC Address'

    # 将 MAC 地址分成三部分，并用破折号连接
    formatted_mac = '-'.join([mac_clean[i:i + 4] for i in range(0, 12, 4)])
    return formatted_mac.upper()


def extract_device_info_from_topo(file_path, encoding='utf-8'):
    try:
        # 尝试不同的编码读取文件
        encodings_to_try = [encoding, 'gbk', 'gb2312', 'iso-8859-1', 'latin-1']
        for enc in encodings_to_try:
            try:
                # 以文本模式读取文件内容，指定编码
                with open(file_path, 'r', encoding=enc) as file:
                    content = file.read()
                print(f"成功使用编码 {enc} 读取文件 {file_path}")
                break
            except UnicodeDecodeError:
                print(f"尝试使用编码 {enc} 读取文件 {file_path} 失败，继续尝试其他编码...")
                continue
        else:
            raise UnicodeDecodeError("无法使用任何已知编码读取文件")

        # 移除XML声明
        content_without_declaration = remove_xml_declaration(content)

        # 解析去掉声明后的内容
        root = ET.fromstring(content_without_declaration)

        # 查找所有 'dev' 元素
        devices = root.find('devices').findall('dev')

        # 提取并返回 设备名, 设备端口号, 设备型号, 设备MAC地址, 以及 settings 中的 -apSN 和 dev id
        return [
            {
                '设备名': device.get('name'),
                '设备端口号': int(device.get('com_port')),  # 将端口号转换为整数以便排序
                '设备型号': device.get('model'),
                '设备MAC地址': device.get('system_mac'),
                'settings': parse_settings(device.get('settings')),
                '设备ID(设备文件夹名)': device.get('id')  # 新增设备ID(设备文件夹名)字段
            } for device in devices
        ]
    except ET.ParseError as e:
        print(f"解析文件 {file_path} 时出错: {e}")
        return []
    except UnicodeDecodeError as e:
        print(f"解码文件 {file_path} 时出错: {e}")
        return []
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")
        return []


def process_all_topo_files_in_current_directory():
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 查找当前目录下所有的 .topo 文件
    topo_files = glob.glob(os.path.join(current_directory, '*.topo'))

    if not topo_files:
        print("当前目录下没有找到 .topo 文件。")
        return

    # 初始化统计变量
    all_devices = []
    model_counter = Counter()
    ap_info = []
    device_category_counter = defaultdict(Counter)

    # 定义分类规则
    category_rules = {
        '交换机': lambda model: model.startswith(('S5700', 'S3700', 'CE6800', 'CE12800')),
        '路由器': lambda model: model.startswith(('AR', 'NE')),
        '防火墙': lambda model: model.startswith(('USG')),
        'WLAN设备': lambda model: model.startswith(('AC', 'AP'))
    }

    # 处理每个 .topo 文件
    for topo_file in topo_files:
        print(f"正在翻译topo文件: {topo_file}")
        results = extract_device_info_from_topo(topo_file)

        if results:
            all_devices.extend(results)  # 将所有设备信息收集到一个列表中
            for device in results:
                # 更新统计信息
                model_counter[device['设备型号']] += 1
                for category, rule in category_rules.items():
                    if rule(device['设备型号']):
                        device_category_counter[category][device['设备型号']] += 1
                        break

                if device['设备型号'].startswith('AP'):
                    ap_info.append({
                        '设备名': device['设备名'],
                        '设备型号': device['设备型号'],
                        'apSN': device['settings'].get('apSN', 'N/A'),
                        'system_mac': format_mac_address(device['设备MAC地址']),
                        '设备ID(设备文件夹名)': device['设备ID(设备文件夹名)']  # 新增设备ID(设备文件夹名)字段
                    })

    # 按设备端口号从小到大排序
    sorted_devices = sorted(all_devices, key=lambda x: x['设备端口号'])

    # 输出 topo 翻译结果
    print("\ntopo翻译结果:")

    # 输出排序后的设备信息
    for device in sorted_devices:
        print(f"  设备名: {device['设备名']}, "
              f"设备端口号: {device['设备端口号']}, "
              f"设备型号: {device['设备型号']}, "
              f"设备MAC地址: {device['设备MAC地址']}, "
              f"设备ID(设备文件夹名): {device['设备ID(设备文件夹名)']}")  # 新增设备ID(设备文件夹名)字段

    # 输出设备总计
    print("\n统计结果:")
    print(f"  设备总计: {len(sorted_devices)}")

    # 输出每个设备型号的总计
    print("  每个设备型号的总计:")
    for model, count in model_counter.items():
        print(f"    {model}: {count}")

    # 输出分类统计结果
    print("\n分类统计结果:")
    for category, models in device_category_counter.items():
        print(f"  {category}:")
        for model, count in models.items():
            print(f"    {model}: {count}")
        print(f"    总计: {sum(models.values())}")

    # 输出 AP 设备的 apSN 和 system_mac
    if ap_info:
        print("\nAP 设备信息:")
        for info in ap_info:
            print(f"  设备名: {info['设备名']}, "
                  f"设备型号: {info['设备型号']}, "
                  f"AP 序列号 (apSN): {info['apSN']}, "
                  f"系统 MAC 地址: {info['system_mac']}, "
                  f"设备ID(设备文件夹名): {info['设备ID(设备文件夹名)']}")  # 新增设备ID(设备文件夹名)字段

    # 生成 MobaXterm Sessions.mxtsessions 文件
    generate_moba_sessions_file(sorted_devices, topo_files)

    # 生成设备信息表 Excel 文件
    generate_device_info_excel(sorted_devices)


def generate_moba_sessions_file(devices, topo_files):
    # 定义 MobaXterm Sessions 文件的路径
    moba_sessions_path = os.path.join(os.getcwd(), 'MobaXterm Sessions.mxtsessions')

    # 读取现有的 MobaXterm Sessions 文件内容
    try:
        with open(moba_sessions_path, 'r', encoding='ansi', errors='replace') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("未找到 MobaXterm Sessions.mxtsessions 文件，将创建一个新的文件。")
        lines = ["[Bookmarks]\n", "SubRep=ENSP\n", "ImgNum=41\n"]

    # 创建一个字典来存储设备名和设备端口号的映射
    device_map = {
        device[
            '设备名']: f"{device['设备名']}=#98#1%127.0.0.1%{device['设备端口号']:04d}%%%2%%%%%0%0%%1080%%%0%-1%0#MobaFont%11%0%0%-1%40%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%0%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1%-1%#0# #-1"
        for device in devices if device['设备端口号'] > 0
    }

    # 替换文件中的设备信息
    new_lines = []
    for topo_file in topo_files:
        topo_file_name = os.path.splitext(os.path.basename(topo_file))[0]
        new_lines.append(f"[Bookmarks]\n")
        new_lines.append(f"SubRep={topo_file_name}\n")
        new_lines.append("ImgNum=41\n")
        for device_name, session_line in device_map.items():
            new_lines.append(f"{session_line}\n")

    # 写入新的 MobaXterm Sessions 文件，使用 ANSI 编码
    with open(moba_sessions_path, 'w', encoding='ansi') as file:
        file.writelines(new_lines)

    print(f"已生成新的 MobaXterm Sessions 文件: {moba_sessions_path}")


def generate_device_info_excel(devices):
    # 创建 DataFrame
    df = pd.DataFrame(devices)

    # 保存为 Excel 文件
    excel_path = os.path.join(os.getcwd(), '设备信息表.xlsx')
    df.to_excel(excel_path, index=False)

    print(f"已生成设备信息表 Excel 文件: {excel_path}")


if __name__ == "__main__":
    # 修改当前工作目录为包含 topo 文件的目录
    process_all_topo_files_in_current_directory()