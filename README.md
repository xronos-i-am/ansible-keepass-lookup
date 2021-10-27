# Lookup KeePass for Ansible

Use the plugin to access KeePass with lookup

## Installation

Dependency: `pykeepass`

    pip install pykeepass --user
    mkdir -p ~/.ansible/plugins/lookup && cd "$_"
    curl https://raw.githubusercontent.com/xronos-i-am/ansible-keepass-lookup/master/keepass.py -o ./keepass.py

## Variables

- `keepass_db_file` - path to KeePass file
- `keepass_password` - password to KeePass 
- `keepass_key_file` - [*optional*] path to keyfile (not tested)

## Usage

Add prompts to playbook:

    vars_prompt:
        - name: keepass_password
        prompt: "Enter keepass DB password"
    private: yes
    - name: keepass_db_file
        prompt: "Enter path to keepass DB"

Use lookups:

    - name: Retrieve entry by path
      debug:
        var: lookup('keepass', 'dir1/dir2/id_rsa')
    - name: Retrieve entries by title
      debug:
        var: lookup('keepass', 'id_rsa', search='title')
    - name: Retrieve entry by username
      debug:
        var: lookup('keepass', 'testuser@test.home', search='username')
    - name: Retrieve entry by uuid
      debug:
        var: lookup('keepass', 'de37072b8cec670ff58212b9cae05806', search='uuid')
    - name: Retrieve entries by tags (list) - not tested!
      debug:
        var: lookup('keepass', {{ ['commerce', 'www'] }}, search='tags')
    - name: Retrieve entries by custom fields (dict)
      debug:
        var: lookup('keepass', {{ {'tag':'ssh-key'} }}, search='custom')

See playbook.yml for details (playbook.sh to run test)
