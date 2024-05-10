import yaml
f=open('switch_remark_pcp_config.yaml','r',encoding='utf-8')

data=yaml.safe_load(f)
print(data)
# print(data['aclaclTable'])