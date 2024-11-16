import requests
import time

# Địa chỉ của Floodlight REST API
FLOODLIGHT_API_URL = 'http://127.0.0.1:8080'

# Hàm lấy thông tin các flow trong Floodlight
def get_flows():
    url = f'{FLOODLIGHT_API_URL}/wm/staticflowpusher/flow/json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching flows: {response.status_code}")
        return {}

# Hàm tính toán server có ít kết nối nhất
def least_connections_server():
    flows = get_flows()
    server_connections = {}

    # Phân tích các flow và tính số lượng kết nối đến mỗi server (hoặc host)
    for flow_id, flow in flows.items():
        # Lấy IP nguồn hoặc đích để xác định server
        src_ip = flow['match']['ipv4_src']
        dst_ip = flow['match']['ipv4_dst']

        if dst_ip not in server_connections:
            server_connections[dst_ip] = 0
        server_connections[dst_ip] += 1

    # Tìm server có ít kết nối nhất
    least_connections = min(server_connections.values(), default=0)
    best_server = [ip for ip, count in server_connections.items() if count == least_connections]

    return best_server[0] if best_server else None

# Hàm chọn server ít kết nối nhất và cập nhật lưu lượng
def load_balancing():
    while True:
        server = least_connections_server()
        if server:
            print(f"Server with least connections: {server}")
            # Thực hiện điều chỉnh flow tại đây nếu cần, ví dụ: thêm flow mới đến server này
            # Hoặc cập nhật lưu lượng từ client
        else:
            print("No server found with least connections.")
        
        time.sleep(5)  # Cập nhật mỗi 5 giây

if __name__ == '__main__':
    load_balancing()

# Tao Flow
# curl -X POST -d '{
#     "flowname":"flow1", 
#     "switch":"00:00:00:00:00:01", 
#     "name":"Flow1", 
#     "cookie":"0", 
#     "priority":"32768", 
#     "active":"true", 
#     "match":{
#         "ipv4_src":"10.0.0.1", 
#         "ipv4_dst":"10.0.0.2"
#     }, 
#     "actions":[{
#         "type":"OUTPUT", 
#         "port":1
#     }]
# }' http://127.0.0.1:8080/wm/staticflowpusher/flow/json
