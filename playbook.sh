# sudo apt install python3 python3.6-dev python3-pip python3-setuptools python3-wheel
# pip3 install ansible pykeepass

python3 $(which ansible-playbook) --extra-vars "keepass_password=test keepass_db_file=./test.kdbx" playbook.yml