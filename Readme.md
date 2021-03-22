# add

## 添加用户时，同一用户cn必须等于uid,不同用户cn/uid/mail必须不同,如果某一参数相同,gitlab同步插件会有问题

```
python3 main.py add '{"cn": ["ep_zhouzw11"],"description": ["ou=ops,ou=users"],"givenName": ["\u5b50\u6587"],"mail": ["xxxxxxx"],"ou": ["ou=users"],"physicalDeliveryOfficeName": ["IT111"],"sn": ["12312"],"telephoneNumber": ["13912311111"],"title": ["\u8fd0\u7ef4"],"uid": ["ep_zhouzw11"],"userPassword": ["213123asda!@#!"]}'
```

# delete
python3 main.py delete '{"uid" : "ep_zhouzw11"}'



# modify
python3 main.py modify '{"uid" : "ep_zhouzw11","password" : "123123!#@ASD"}'
