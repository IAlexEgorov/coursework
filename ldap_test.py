from ldap3 import Connection, Server

user = "bot.admin"
password = "DEVpassword"
server = Server('ipa.web-bee.loc', use_ssl=True)

conn = Connection(server, user="uid=bot.admin,cn=users,cn=accounts,dc=web-bee,dc=loc", password=password)
print(conn.entries[0])
