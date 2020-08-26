# !/usr/bin/python3
# -*-encoding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:         LdapSyncZenTao.py
# Description:  Synchronous LDAP for Zen account
# Author:       herrywen
# Date:         2020/7/13
# -------------------------------------------------------------------------------


import json
import logging
from ldap3.utils.hashed import hashed
from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE, MODIFY_DELETE, HASHED_MD5



'''
        

        1.Usage:
            python main.py add json文件
            python main.py modify uid newpasswd
            python main.py delete uid
            
        2.错误日志名称: LdapSyncZenTaoError.log
'''


logging.basicConfig(filename='LdapSyncZenTaoError.log',level=logging.ERROR,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y/%m/%d %H:%M:%S')

class ldap(object):
    def __init__(self):
        self.url = 'ldap://172.21.100.31:389'
        self.base_dn = 'dc=little,dc=cn'
        self.manager_account = 'cn=admin,dc=little,dc=cn'
        self.manager_passwd = '13212'
        self.ldap_obj = None
        self.ldap_conn(self.manager_account, self.manager_passwd)


    def ldap_conn(self,user,passlittlerd):
        server = Server(self.url)
        conn = Connection(server, user, passlittlerd, auto_bind=True)
        self.ldap_obj = conn

    def ldap_search(self,uid):
        search_uid = "(&(objectclass=person)(uid={}))".format(uid)
        success = self.ldap_obj.search(self.base_dn, search_uid, attributes=['*'])
        if not success:
            msg = 'The current {} user does not exist'.format(uid)
            logging.error(msg)
        if len(self.ldap_obj.entries[0].entry_to_json()) > 0:
            RESULT = json.loads(self.ldap_obj.entries[0].entry_to_json())
        return RESULT['dn']


    def ldap_getUidNumber(self):
        search_filter = "(objectclass=person)"
        success = self.ldap_obj.search(self.base_dn, search_filter, attributes=['uidNumber'])
        if not success:
            msg = 'The operation requested failed due to netlittlerk problems!'
            logging.error(msg)
        AllUidNumberList = []
        for i in self.ldap_obj.entries:
            if len(i.entry_to_json()) > 0:
                RESULT = json.loads(i.entry_to_json())
                AllUidNumberList.append(RESULT['attributes']['uidNumber'][0])
        return max(AllUidNumberList)

    def ldap_getGidNumber(self,description):
        ou = description.split(',')[0].split('=')[-1]
        search_gid = "(&(objectclass=posixGroup)(cn={}))".format(ou)
        success = self.ldap_obj.search(self.base_dn, search_gid, attributes=['gidNumber'])
        if not success:
            msg = 'The PosixGroup {} can be not exist, Please Checkout your configuration!'.format(ou)
            logging.error(msg)
        if len(self.ldap_obj.entries[0].entry_to_json()) > 0:
            RESULT = json.loads(self.ldap_obj.entries[0].entry_to_json())
        return RESULT['attributes']['gidNumber'][0]

    def ldap_add(self, uid, sn, givenName, description, mail, physicalDeliveryOfficeName, telephoneNumber, title, userPasslittlerd):
        '''
        1.object_classes['uidObject']
            Superior: top
            Must contain attributes: uid
        2.object_classes['person']
            Superior: top
            Must contain attributes: sn, cn
            May contain attributes: userPasslittlerd, telephoneNumber, seeAlso, description
        3.object_classes['organizationalPerson']
            Superior: person
            May contain attributes: title, x121Address, registeredAddress, destinationIndicator, preferredDeliveryMethod, telexNumber, teletexTerminalIdentifier, telephoneNumber, internationaliSDNNumber, facsimileTelephoneNumber, street, postOfficeBox, postalCode, postalAddress, physicalDeliveryOfficeName, ou, st, l
        4.object_classes['top']
            Must contain attributes: objectClass
        5.object_classes['inetOrgPerson']
            Superior: organizationalPerson
            May contain attributes: audio, businessCategory, carLicense, departmentNumber, displayName, employeeNumber, employeeType, givenName, homePhone, homePostalAddress, initials, jpegPhoto, labeledURI, mail, manager, mobile, o, pager, photo, roomNumber, secretary, uid, userCertificate, x500uniqueIdentifier, preferredLanguage, userSMIMECertificate, userPKCS12
        :param uid: str
        :param sn:  str
        :param givenName: str
        :return: bool值，True或者False

        6.example:
            {
	            "attributes": {
                "cn": ["ep_zhouzw"],
                "description": ["ou=ops,ou=users"],
                "givenName": ["\u5b50\u6587"],
                "mail": ["xxx"],
                "objectClass": ["person", "top", "uidObject", "inetOrgPerson", "organizationalPerson"],
                "ou": ["ou=users"],
                "physicalDeliveryOfficeName": ["IT\u652f\u6491\u7ec4"],
                "sn": ["\u5468"],
                "telephoneNumber": ["xxxxxxxx"],
                "title": ["\u8fd0\u7ef4"],
                "uid": ["ep_zhouzw"],
                "userPasslittlerd": ["xxxxxxxxx"]
            },
	        "dn": "uid=ep_zhouzw,ou=ops,ou=users,dc=little,dc=cn"
            }


        '''
        dn = "cn={}".format(uid[0]) + "," + str(description[0]) + "," + self.base_dn
        object_class = [
            "inetOrgPerson",
            "person",
            "top",
            "uidObject",
            "organizationalPerson"
        ]
        attributes = {
            "cn": [
                str(uid[0])
            ],
            "description": [
                str(description[0])
            ],
            "givenName": [
                str(givenName[0])
            ],
            "mail": [
                str(mail[0])
            ],
            "ou": [
                "ou=users"
            ],
            "physicalDeliveryOfficeName": [
                str(physicalDeliveryOfficeName[0])
            ],
            "sn": [
                str(sn[0])
            ],
            "telephoneNumber": [
                int(telephoneNumber[0])
            ],
            "title": [
                str(title[0])
            ],
            "uid": [
                str(uid[0])
            ],
            "userPasslittlerd": [
                str(userPasslittlerd[0])
            ]
        }
        success = self.ldap_obj.add(dn=dn, object_class=object_class, attributes=attributes, controls=None)
        if not success:
            msg = "User {} creation failed, required parameters are missing, or the same user already exists in LDAP".format(uid[0])
            logging.error(msg)


    def ldap_modify(self,uid,newpasswd):
        dn = self.ldap_search(uid)
        hashed_passwd = hashed(HASHED_MD5, newpasswd)
        changes = {
            'userPasslittlerd': [(MODIFY_REPLACE, [hashed_passwd])]
        }
        success = self.ldap_obj.modify(dn=dn, changes=changes, controls=None)
        if not success:
            msg = 'Ubable to change Passlittlerd for %s'.format(uid)
            logging.error(msg)

    def ldap_delete(self,uid):
        dn = self.ldap_search(uid)
        success = self.ldap_obj.delete(dn=dn, controls=None)
        if not success:
            msg = 'Unable to delete user {}'.format(uid)
            logging.error(msg)

