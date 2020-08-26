# -*-encoding:utf-8-*-
import sys
import json
from LdapSyncZenTao import ldap


y = ldap()

# 添加用户操作
if sys.argv[1] == 'add':
    if len(sys.argv[2]) > 0:
        RESULT = json.loads(sys.argv[2])
        print(RESULT)
        y.ldap_add(RESULT['uid'], RESULT['sn'], RESULT['givenName'], RESULT['description'], RESULT['mail'],
                   RESULT['physicalDeliveryOfficeName'], RESULT['telephoneNumber'], RESULT['title'],
                   RESULT['userPassword'])

# 修改用户密码操作
elif sys.argv[1] == 'modify':
    if len(sys.argv[2]) > 0:
        RESULT = json.loads(sys.argv[2])
        y.ldap_modify(RESULT['uid'], RESULT['password'])

# 删除用户操作
elif sys.argv[1] == 'delete':
    if len(sys.argv[2]) > 0:
        RESULT = json.loads(sys.argv[2])
        y.ldap_delete(RESULT['uid'])
