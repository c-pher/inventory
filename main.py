__author__ = 'Andrey Komissarov'
__date__ = '06.2020'

import json
import warnings
from concurrent.futures.thread import ThreadPoolExecutor

import requests

warnings.filterwarnings('ignore')


username = None
password = None


def get_current_power_state(ip):
    url = f'https://{ip}/redfish/v1/Systems/System.Embedded.1/'
    try:
        response = requests.get(url, verify=False, auth=(username, password))
        data = response.json()

        with open('inventory.txt', 'a') as f:
            f.write(f'iDRAC IP: {ip}\n')
            f.write(f'HostName: {data["HostName"]}\n')
            f.write(f'CPU: {data["ProcessorSummary"]["Model"]}\n')
            f.write(f'MemorySummary: {data["MemorySummary"]["TotalSystemMemoryGiB"]} GB\n')
            f.write(f'Model: {data["Model"]}\n')
            f.write(f'PartNumber: {data["PartNumber"]}\n')
            f.write(f'SKU: {data["SKU"]}\n')
            f.write(f'SerialNumber: {data["SerialNumber"]}\n')
            f.write(f'Status: {data["Status"]["Health"]}\n\n')

        # print(data)
        print(f'iDRAC IP: {ip}')
        print(f'HostName: {data["HostName"]}')
        print(f'CPU: {data["ProcessorSummary"]["Model"]}')
        print(f'MemorySummary: {data["MemorySummary"]["TotalSystemMemoryGiB"]} GB')
        print(f'Model: {data["Model"]}')
        print(f'PartNumber: {data["PartNumber"]}')
        print(f'SKU: {data["SKU"]}')
        print(f'SerialNumber: {data["SerialNumber"]}')
        print(f'Status: {data["Status"]["Health"]}')
        print('============')

    except requests.exceptions.ConnectionError:
        print(f'Host {ip} is unreachable or failed to login!')
    except json.decoder.JSONDecodeError:
        print('Cannot decode response.')


with open('ip') as file:
    ips = [ip.strip() for ip in file.readlines()]

    with ThreadPoolExecutor(max_workers=128) as pool:
        for _ in pool.map(get_current_power_state, ips):
            pass
