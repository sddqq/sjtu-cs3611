import RestApi
import json

match = {
    "nw_dst":"223.1.2.2",
    "dl_type":2048,
    "nw_proto":17
}
print(RestApi.add_flow_entry(2, match, 32769, [{"actions":"drop"}]))

match = {  
    "in_port": 1, 
    "dl_type": 2048, 
    "ipv4_src": "223.1.2.2",
} 
actions = [  
    {  
        "type": "SET_FIELD",  
        "field": "ipv4_dst",  
        "value": "223.1.1.2" 
    },  
    {  
        "type": "OUTPUT",  
        "port": 2   
    }  
]  
print(RestApi.add_flow_entry(2, match, 32769, actions))