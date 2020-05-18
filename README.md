# Dynatrace Management Zones
Support via configuration as code (CaC) the creation of new Management Zones within Dynatrace

# Requirements

To use this requires the following:

    ansible ~= 2.9.x
	python ~= 2.7.x

You will then need to supply the playbook with two critical pieces of information:

    The environment URL: Managed https://{your-domain}/e/{your-environment-id} | SaaS https://{your-environment-id}.live.dynatrace.com
    The PaaS token of your environment for downloading the OneAgent installer

Example Playbook
----------------

Most basic Dynatrace Management Zone with a simple rule

```bash
---
- hosts: localhost
  vars:
    dynatrace_environment_url: {your-environment-id}.live.dynatrace.com
    dynatrace_paas_token: {your-paas-token}
```

Testing
-------

To test this playbook, follow the steps below:

1) Define required variables in `dynatrace.yml` file. For example:

```bash
---
- hosts: localhost
  vars:
    environment_url: https://{your-environment-id}.live.dynatrace.com
    paas_token: {your-paas-token}
```

2) Define the name of your Management zone in mzone.json. For example:

```bash
{
  "name": "Management-Zone-Name",
  "rules": [
    {
      "type": "HOST",
      "enabled": true,
      "propagationTypes": [
        "HOST_TO_PROCESS_GROUP_INSTANCE"
      ]
```
	
3) From your linux machine, where the Github repository is cloned type the following:

```bash
	~$ pip install jmespath
    ~$ ansible-playbook /path_to_ansible_playbook/dynatrace.yml
```

4) Expected result should be similar to the following:

```bash
PLAY [Support via configuration as code (CaC) the creation of new Management Zones within Dynatrace] **************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************
ok: [localhost]

TASK [Get existing dynatrace management zones] ********************************************************************************************************************************************************************
ok: [localhost]

TASK [set_fact] ***************************************************************************************************************************************************************************************************
skipping: [localhost] => (item=AllianzTest)
skipping: [localhost] => (item=AllianzTest3)

TASK [Create a dynatrace management zone] *************************************************************************************************************************************************************************
[WARNING]: The value False (type bool) in a string field was converted to u'False' (type string). If this does not look like what you expect, quote the entire value to ensure it does not change.
ok: [localhost]

PLAY RECAP ********************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```
