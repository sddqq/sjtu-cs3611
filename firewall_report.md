# 4.2 FireWall Report

- 最初想法：利用ryu.app.rest_firewall配置交换机的防火墙，但是发现ryu提供的防火墙首先会禁用所有数据传输，而后配置允许的数据传输，但是我们想要实现的功能是在首先允许传输的情况下，配置禁止传输的规则，又发现ryu自带的firewall实际上也是由配置流表实现的，故直接对流表进行配置，以实现防火墙功能。

- 代码实现
    ```
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
    ```
    利用restapi接口，实现对流表的便捷修改，通过match数据包的来源和目的地进行阻截，实现了拒绝来自某IP地址的数据包、拒绝试图访问某个主机的数据包的功能。  

    
    ```
    def clear_firewall_rule(switch_id):
    cookie = 0x666
    url = "http://127.0.0.1:8080/stats/flowentry/delete"
    data_ = {
        "dpid":switch_id,
        "cookie":cookie
    }
    req = requests.post(url,data=data_)
    return req.status_code
    ```
    该清除函数想法为，利用先前add_flow_entry添加的流表cookie的特殊性，筛选出手动添加的防火墙流表并进行删除，以达到删除已配置的firewall_rule的目的，但是restapi提供的删除接口似乎总是删除交换机的整个流表，而不单单删除单一表项，故该功能暂未实现