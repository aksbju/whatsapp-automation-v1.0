# whatsapp-automation-v1.0
 
 requirements excluding standard library
 
     selenium
     
 Installation with PIP
 
     pip install selenium 
     
 Import
 
     import whatsapp
     
 Initialize
 
     wapp = whatsapp()
     wapp.initialize('chromedriver.exe') # chromedriver path
     
 Closing Webdriver
 
     wapp.close()
     
 Authentication
 
     if wapp.check_auth() == False:
         qr_image = wapp.get_qr_code() # base64 image data
 
 Deauthentication
 
     if wapp.check_auth() == True:
         wapp.logout()
     
 Send text
 
     if wapp.check_auth() == True:
         wapp.send_text('91XXXXXXXXXX', 'MESSAGE')
         
 Send attachment
 
     if wapp.check_auth() == True:
         wapp.send_text('91XXXXXXXXXX', '%userprofile%/desktop/file.extension')
         
