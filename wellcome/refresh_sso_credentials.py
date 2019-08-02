#!/usr/bin/env python
# -*- encoding: utf-8

import io
import pathlib
import struct
import time


COOKIES_PATH = pathlib.Path.home() / "Library" / "Cookies" / "Cookies.binarycookies"


def read_cookies(binary_file):
    # Based on http://www.securitylearn.net/2012/10/27/cookies-binarycookies-reader/
    if binary_file.read(4) != b"cook":
        raise ValueError("Not a Cookies.binarycookies file?")

    num_pages=struct.unpack('>i',binary_file.read(4))[0]               #Number of pages in the binary file: 4 bytes

    page_sizes=[]
    for np in range(num_pages):
    	page_sizes.append(struct.unpack('>i',binary_file.read(4))[0])  #Each page size: 4 bytes*number of pages

    pages=[]
    for ps in page_sizes:
    	pages.append(binary_file.read(ps))                      #Grab individual pages and each page will contain >= one cookie

    for page in pages:
    	page=io.BytesIO(page)                                     #Converts the string to a file. So that we can use read/write operations easily.
    	page.read(4)                                            #page header: 4 bytes: Always 00000100
    	num_cookies=struct.unpack('<i',page.read(4))[0]                #Number of cookies in each page, first 4 bytes after the page header in every page.

    	cookie_offsets=[]
    	for nc in range(num_cookies):
    		cookie_offsets.append(struct.unpack('<i',page.read(4))[0]) #Every page contains >= one cookie. Fetch cookie starting point from page starting byte

    	page.read(4)                                            #end of page header: Always 00000000

    	cookie=''
    	for offset in cookie_offsets:
    		page.seek(offset)                                   #Move the page pointer to the cookie starting point
    		cookiesize=struct.unpack('<i',page.read(4))[0]             #fetch cookie size
    		cookie=io.BytesIO(page.read(cookiesize))              #read the complete cookie

    		cookie.read(4)                                      #unknown

    		flags=struct.unpack('<i',cookie.read(4))[0]                #Cookie flags:  1=secure, 4=httponly, 5=secure+httponly
    		cookie_flags=''
    		if flags==0:
    			cookie_flags=''
    		elif flags==1:
    			cookie_flags='Secure'
    		elif flags==4:
    			cookie_flags='HttpOnly'
    		elif flags==5:
    			cookie_flags='Secure; HttpOnly'
    		else:
    			cookie_flags='Unknown'

    		cookie.read(4)                                      #unknown

    		urloffset=struct.unpack('<i',cookie.read(4))[0]            #cookie domain offset from cookie starting point
    		nameoffset=struct.unpack('<i',cookie.read(4))[0]           #cookie name offset from cookie starting point
    		pathoffset=struct.unpack('<i',cookie.read(4))[0]           #cookie path offset from cookie starting point
    		valueoffset=struct.unpack('<i',cookie.read(4))[0]          #cookie value offset from cookie starting point

    		endofcookie=cookie.read(8)                          #end of cookie

    		expiry_date_epoch= struct.unpack('<d',cookie.read(8))[0]+978307200          #Expiry date is in Mac epoch format: Starts from 1/Jan/2001
    		expiry_date=time.strftime("%a, %d %b %Y ",time.gmtime(expiry_date_epoch))[:-1] #978307200 is unix epoch of  1/Jan/2001 //[:-1] strips the last space

    		create_date_epoch=struct.unpack('<d',cookie.read(8))[0]+978307200           #Cookies creation time
    		create_date=time.strftime("%a, %d %b %Y ",time.gmtime(create_date_epoch))[:-1]
    		#print create_date

    		cookie.seek(urloffset-4)                            #fetch domaain value from url offset
    		url=''
    		u=cookie.read(1)
    		while struct.unpack('<b',u)[0]!=0:
    			url=url+str(u)
    			u=cookie.read(1)

    		cookie.seek(nameoffset-4)                           #fetch cookie name from name offset
    		name=''
    		n=cookie.read(1)
    		while struct.unpack('<b',n)[0]!=0:
    			name=name+str(n)
    			n=cookie.read(1)

    		cookie.seek(pathoffset-4)                          #fetch cookie path from path offset
    		path=''
    		pa=cookie.read(1)
    		while struct.unpack('<b',pa)[0]!=0:
    			path=path+str(pa)
    			pa=cookie.read(1)

    		cookie.seek(valueoffset-4)                         #fetch cookie value from value offset
    		value=''
    		va=cookie.read(1)
    		while struct.unpack('<b',va)[0]!=0:
    			value=value+str(va)
    			va=cookie.read(1)

    		print('Cookie : '+name+'='+value+'; domain='+url+'; path='+path+'; '+'expires='+expiry_date+'; '+cookie_flags)




if __name__ == "__main__":
    read_cookies(COOKIES_PATH.open("rb"))
