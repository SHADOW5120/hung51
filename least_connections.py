import requests
import json

# Địa chỉ IP của Floodlight Controller
CONTROLLER_IP = "127.0.0.1"
CONTROLLER_PORT = "8080"

# Danh sách server và số kết nối của mỗi server
servers = {
    "10.0.0.1": 0,
    "10.0.0.2": 0,
    "10.0.0.3": 0
}

def get_least_connections_server():
    # Chọn server có ít kết nối nhất
    return min(servers, key=servers.get)

def install_flow(src_ip, dst_ip, switch_id, out_port):
    url = f"http://{CONTROLLER_IP}:{CONTROLLER_PORT}/wm/staticflowpusher/json"
    flow = {
        "switch": switch_id,
        "name": f"flow-{src_ip}-{dst_ip}",
        "priority": "100",
        "eth_type": "0x0800",
        "ipv4_src": src_ip,
        "ipv4_dst": dst_ip,
        "active": "true",
        "actions": f"output={out_port}"
    }

    response = requests.post(url, data=json.dumps(flow))
    if response.status_code == 200:
        print(f"Flow installed: {src_ip} -> {dst_ip}")
    else:
        print(f"Failed to install flow: {response.text}")

def release_connection(server_ip):
    # Giảm số kết nối khi kết thúc
    if server_ip in servers:
        servers[server_ip] -= 1

def main():
    while True:
        # Giả lập gói tin mới
        src_ip = "10.0.0.4"  # IP của client
        dst_ip = get_least_connections_server()

        # Tăng số kết nối cho server đã chọn
        servers[dst_ip] += 1

        # Cài đặt flow vào switch
        switch_id = "00:00:00:00:00:00:00:01"  # ID của switch
        out_port = 2  # Giả định port tương ứng
        install_flow(src_ip, dst_ip, switch_id, out_port)

        # In trạng thái server
        print(f"Current server connections: {servers}")

if __name__ == "__main__":
    main()
