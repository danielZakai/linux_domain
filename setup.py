#!/usr/bin/python
import os
project = input('Enter the name of the project: ')
#create project folder setup
os.system('mkdir ' + project)
tfPath = './terraform/infa/'
configPath = './terraform/config/'
projectPath = './'+project+'/'
projectConfigPath = projectPath+'conf/'
os.system('mkdir '+ projectConfigPath)
#create RBAC script setup
users = []
hosts = []
gather = ' '
#Enter the users
print('Enter the IPA users for this project')
while gather != 'done':
                gather = input('Enter a user to give access to or "done" to continue: ')
                if gather != "done":
                        users.append(gather)


explain = ''' At each promt, enter the alias of the machine you wish to create. If creating more than one type of machine, enter the alias
             with numer two or three after. A maximum of three machines per each type can be made per project
             For 2 redirectors, choose both the "red" and "red2" options'''
usage = '''
        Recon machine  = rec  | Phishing machine  = phish  | Second redirector = red2
        Post Exploit   = post | Redirector server = red    | CryptPad Server   = crypt
        Exploit server = exp  | Managment machine = m      | RedElk Sever      = elk
'''
user_input = ' '
print(explain)
print(usage)
while user_input != 'done':
        user_input = input('Enter the alias of machine you want to create or done to finish: ')
        if user_input == 'rec':
                os.system('cp '+tfPath+ 'recon_machine.tf '+projectPath)
                os.system('cp '+configPath+'config_recon.tf '+ projectConfigPath+'config_recon.tf')
                hosts.append(project+'-recon.cast.local')
        elif user_input == 'elk':
                os.system('cp '+tfPath+'redelk.tf '+projectPath)
                os.system('cp '+configPath+'config_redelk.tf '+projectConfigPath+'config_redelk.tf')
                hosts.append(project+'redelk.cast.local')
        elif user_input == 'crypt':
                os.system('cp '+tfPath+'cryptpad.tf '+projectPath)
                os.system('cp '+configPath+'config_crypt.tf '+projectConfigPath+'config_crypt.tf')
                hosts.append(project+'cryptpad.cast.local')
        elif user_input == 'post':
                os.system('cp '+tfPath+'postExploit_machine.tf '+projectPath)
                os.system('cp '+configPath+'config_post.tf '+projectConfigPath+'config_post.tf')
                hosts.append(project+'-postexploit.cast.local')
        elif user_input == 'phish':
                os.system('cp ' +tfPath+'phishing_machine.tf '+ projectPath)
                os.system('cp '+configPath+'config_phishing.tf '+ projectConfigPath+'config_phishing.tf')
                hosts.append(project+'-phishing.cast.local')
        elif user_input == 'exp':
                os.system('cp '+tfPath+'exploit_machine.tf '+ projectPath)
                os.system('cp ' +configPath+'config_exploit.tf '+projectConfigPath+'config_exploit.tf')
                hosts.append(project+'-exploit.cast.local')
        elif user_input == 'red':
                os.system('cp '+tfPath+ 'redirector_machine.tf ' + projectPath)
                os.system('cp '+configPath+'config_redirector.tf '+projectConfigPath+'config_redirector.tf')
        elif user_input == 'red2':
                os.system('cp '+tfPath+ 'redirector_2_machine.tf ' +projectPath)
                os.system('cp '+configPath+'config_2_redirector.tf '+projectConfigPath+'config_2_redirector.tf')
        elif user_input == 'm':
                os.system('cp ' + tfPath+'mgmt_machine.tf ' + projectPath)
                os.system('cp '+configPath+'config_mgmt.tf ' + projectConfigPath+'config_mgmt.tf')
                hosts.append(project+'-mgmt.cast.local')
        elif user_input == 'done':
                break
        else:
                print ('invalid input')

hbac = open('hbac.sh', 'w+')
hbac.write('ipa hostgroup-add '+ project+'-hosts')
for i in hosts:
        hbac.write('\nipa hostgroup-add-member ' +project+'-hosts --hosts='+i)
hbac.write('\nipa group-add '+ project+'-users')
for i in users:
        hbac.write('\nipa group-add-member ' +project+'-users --users='+i)
hbac.write('\nipa hbacrule-add '+project+'-hbac')
hbac.write('\nipa hbacrule-add-host '+project+'-hbac --hostgroup '+project+'-hosts')
hbac.write('\nipa hbacrule-add-user '+project+'-hbac --group '+project+'-users')
os.system('mv hbac.sh '+projectPath)

os.system('cp '+tfPath+'RG_and_vnet.tf '+projectPath)
os.system('cp '+tfPath+'subnet.tf '+projectPath)
f = open('vars.tf', 'w+')
f.write('variable "project" {\n type = string\n default = "'+project+ '"\n}')
os.system('mv vars.tf '+projectPath)
os.system('cp ' + tfPath+'deploy.sh ' + projectPath)
os.system('cp ' + tfPath+'destroy.sh ' + projectPath)
os.system('cp ./ansible/freeipa/hbac.yml '+ projectPath)
