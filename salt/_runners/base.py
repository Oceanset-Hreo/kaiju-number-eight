import json
import os

import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import salt.client

salt_config_file = "/etc/salt/master"
# Initialize the Slack WebClient with your token
slack_token = os.getenv("SLACK_TOKEN")
client = WebClient(token=slack_token)


class CmdException(Exception):
    def __init__(self, node=None, stderr=None, stdout=None, unknown_e=None):
        self.node = node
        self.stderr = stderr
        self.stdout = stdout
        self.unknown_e = unknown_e

        super(CmdException, self).__init__(self.stderr or self.unknown_e)


def salt_local_client():
    """https://docs.saltproject.io/en/3003/ref/clients/index.html

    Usage:
        >>> salt_local_client().cmd('web*', 'cmd.run', ['su - pinkoi -c "cd /var/www/pinkoi && git reset --hard && git clean -f"'])
    """

    return salt.client.LocalClient(salt_config_file)


def cmd2(*args, **kwargs):
    cmd_kwargs = kwargs.pop("cmd_kwargs", None)
    return salt_local_client().cmd(full_return=True, kwarg=cmd_kwargs, *args, **kwargs)


def check_cmd_status_n_raise(return_val):
    """
    return_val

    {
        'staging001': {
            'jid': '20180820160131391821',
            'retcode': 0,
            'ret': {
                'pid': 51168,
                'retcode': 0,
                'stderr': '',
                'stdout': 'bin\nboot\ndev\netc\nhome\ninitrd.img\ninitrd.img.old\njupyterhub.sqlite\njupyterhub_cookie_secret\nlib\nlib64\nlost+found\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar\nvmlinuz\nvmlinuz.old',
            },
        }
    }
    """

    try:
        for node, result in return_val.items():
            print("check_cmd_status_n_raise", node, result)
            if result["retcode"]:
                if isinstance(result["ret"], str):
                    raise CmdException(node=node, stderr=result["ret"])
                else:
                    if "out" in result and result["out"] == "highstate":
                        for state_result in result["ret"].values():
                            if state_result["result"] is True:
                                continue

                            raise CmdException(
                                node=f'{node} / {state_result["comment"]}',
                                stderr=state_result["changes"]["stderr"],
                                stdout=state_result["changes"]["stdout"],
                            )

                    raise CmdException(
                        node=node,
                        stderr=result["ret"]["stderr"],
                        stdout=result["ret"]["stdout"],
                    )

    except CmdException as e:
        raise e

    except Exception as e:
        raise CmdException(unknown_e=e)

    return return_val


def cmd_n_raise2(*args, **kwargs):
    return check_cmd_status_n_raise(cmd2(*args, **kwargs))


# - notification helpers - #


def send_slack(
    text,
):

    try:
        response = client.chat_postMessage(channel="#water-explorer-one-v2", text=text)
        return response
    except Exception as e:
        print("try catch", str(e))


if __name__ == "__main__":
    send_slack("hello")
