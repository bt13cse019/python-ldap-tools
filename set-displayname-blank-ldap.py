# Author : Simon Brennan
# Language : Python 2.x
# Description : Update displayName attribute to None. Easily modified for other purposes.
# Requires python-ldap module.

import ldap

try:
	#Open a connection to the LDAP server.
	l = ldap.open("localhost",1389)
	## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
	## and do a bind as shown in the above example.
	# you can also set this to ldap.VERSION2 if you're using a v2 directory
	# you should  set the next option to ldap.VERSION2 if you're using a v2 directory
	l.protocol_version = ldap.VERSION3	
	#bind as manager if you need to perform write tasks. Otherwise anonymous will do for a read!
	l.simple_bind_s("cn=Manager","test")
except ldap.LDAPError, e:
	print e
	# print the ldap error if something broke.


## The next lines will also need to be changed to support your search requirements and directory
baseDN = "dc=example"
searchScope = ldap.SCOPE_SUBTREE
## retrieve all attributes - again adjust to your needs - see documentation for more options
retrieveAttributes = None
searchFilter = "objectclass=person"

#Get a list of everyone in LDAP, place them into a tuple.
print "Getting a list of everyone in ldap... \n"

try:
        entries = 0
        ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
        result_set = []
        while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                        break
                else:
                        ## here you don't have to append to a list
                        ## you could do whatever you want with the individual entry
                        ## The appending to list is just for illustration. 
                        if result_type == ldap.RES_SEARCH_ENTRY:
				result_set.append(result_data)
                        entries = entries + 1
	#result_set contains the contents of the ldap query
 	#entries returns the number of entries returned from ldap.

except ldap.LDAPError, error:
        print error

print "All good... replacing displayName with None."

#This will break up the tuple into individual variables based on the supplied key by
#interrating through the tuples and pulling out the required keys
#The code below will set the display name to None on all accounts.
try:
	for i in range(len(result_set)):
		for entry in result_set[i]:
			uid = entry[1]['uid'][0]
			mod_attrs = [( ldap.MOD_REPLACE, "displayName", None)]
			dn = "uid="+ uid + ",ou=People,dc=example"
			l.modify_s(dn, mod_attrs)
except ValueError:
	print "Oops! something broke while decoding the LDAP tuples... run!"

print "Completed successfully!"
