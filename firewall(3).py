import requests
import heapq
import json
import urllib.request
import urllib
def get_all_switches():
    url="http://127.0.0.1:8080/v1.0/topology/switches"
    req=urllib.request.Request(url)
    res_data=urllib.request.urlopen(req)
    res=res_data.read()
    res=json.loads(res)
    return res

def get_all_links():
    url="http://127.0.0.1:8080/v1.0/topology/links"
    req=urllib.request.Request(url)
    res_data=urllib.request.urlopen(req)
    res = res_data.read()
    res =json.loads(res)
    return res

def get_switch(dpid):
    url="http://127.0.0.1:8080/v1.0/topology/switches/"+dpid
    req=urllib.request.Request(url)
    res_data=urllib.request.urlopen(req)
    res=res_data.read()
    res=json.loads(res)
    return res

def get_hosts(dpid):
    url="http://127.0.0.1:8080/v1.0/topology/hosts/"+dpid
    req=urllib.request.Request(url)
    res_data=urllib.request.urlopen(req)
    res=res_data.read()
    res=json.loads(res)
    return res

def add_flow_entry(dpid,match,priority,actions):
    url="http://127.0.0.1:8080/stats/flowentry/add"
    post_data=json.dumps({
        'dpid':dpid,
        'match':match,
        'priority':priority,
        'actions':actions
    }).encode('utf-8')
    req=urllib.request.Request(url,data=post_data,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req) as response:
        return response.getcode()
    
def block_ip(switch_id, ip_address):
    match = {
        "nw_src": ip_address
    }
    actions = []
    add_flow_entry(switch_id, match, 65535, actions)

def block_host(switch_id, host_ip):
    match = {
        "nw_dst": host_ip
    }
    actions = []
    add_flow_entry(switch_id, match, 65535, actions)

def block_keyword(switch_id, keyword):
    # Assuming the firewall supports payload keyword matching
    # If not supported directly by the firewall, this would require a more complex setup
    match = {
        "tp_src": keyword  # This is a placeholder; actual implementation may vary
    }
    actions = []
    add_flow_entry(switch_id, match, 100, actions)

def main():
    while True:
        print("\nFirewall Management Menu")
        print("1. Block IP Address")
        print("2. Block Host")
        print("3. Block Keyword")
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
            switch_id = input("Enter switch ID: ")
            keyword = input("Enter keyword to block: ")
            block_keyword(switch_id, keyword)
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()