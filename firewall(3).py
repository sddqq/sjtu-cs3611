import requests
import heapq
import json
import urllib.request
import urllib
import urllib
def delete_flow_entry(dpid, match=None, priority=None, actions=None):
    url = "http://127.0.0.1:8080/stats/flowentry/delete"
    post_data = "{'dpid':%s" % dpid
    if match is not None:
        post_data += ",'match':%s" % str(match)
    if priority is not None:
        post_data += ",'priority':%s" % 65535
    if actions is not None:
        post_data += ",'actions':%s" % str(actions)
    post_data += "}"
    req = requests.post(url,data=post_data)
    return req.status_code

def add_flow_entry(dpid,match,priority,actions):
    url="http://127.0.0.1:8080/stats/flowentry/add"
    post_data=json.dumps({
        'cookie':0x666,
        'dpid':dpid,
        'match':match,
        'priority':priority,
        'actions':actions
    }).encode('utf-8')
    req=urllib.request.Request(url,data=post_data,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req) as response:
        return response.getcode()
    
def block_ip(switch_id, ip_address):
    match = json.dumps({
        "nw_src": ip_address,
        "dl_type": 2048
    })

    actions = []
    add_flow_entry(switch_id, match, '65535', actions)

def block_host(switch_id, host_ip):
    match = {
        "nw_dst": host_ip,
        "dl_type": 2048
    }
    actions = []
    add_flow_entry(switch_id, match, '65535', actions)

def block_keyword(switch_id, keyword):
    # todo
    match = {
        "tp_src": keyword  # This is a placeholder; actual implementation may vary
    }
    actions = []
    add_flow_entry(switch_id, match, 100, actions)

def clear_firewall_rule(switch_id):
    cookie = 0x666
    url = "http://127.0.0.1:8080/stats/flowentry/delete"
    data_ = {
        "dpid":switch_id,
        "cookie":cookie
    }
    req = requests.post(url,data=data_)
    return req.status_code

def main():
    while True:
        print("\nFirewall Management Menu")
        print("1. Block IP Address")
        print("2. Block Host")
        print("3. Clear FireWall Rule")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            switch_id = input("Enter switch ID: ")
            ip_address = input("Enter IP address to block: ")
            block_ip(switch_id, ip_address)
        elif choice == '2':
            switch_id = input("Enter switch ID: ")
            host_ip = input("Enter host IP address to block: ")
            block_host(switch_id, host_ip)
        elif choice == '3':
            switch_id = input("Enter switch ID to clear: ")
            c = delete_flow_entry(switch_id,priority=65535,actions="drop")
            if c == 200:
                print("Firewall rules of switch{} is cleared sucessfully".format(switch_id))
            else:
                print("Firewall rules of switch{} is failed to clear".format(switch_id))
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()