import time

import base


class DeployMessenger:
    def __init__(
        self,
        action: str,
        start_emoji: str = ":airplane_departure:",
        end_emoji: str = ":rocket:",
        fail_emoji: str = ":boom:",
        channel: str = "#koi-bus",
    ):
        self.action: str = action
        self.start_emoji: str = start_emoji
        self.end_emoji: str = end_emoji
        self.fail_emoji: str = fail_emoji
        self.channel: str = channel
        self.start_ts: float = None
        self.end_ts: float = None

    @property
    def elapsed(self) -> float:
        if any(x is None for x in (self.start_ts, self.end_ts)):
            return 0.0

        return self.end_ts - self.start_ts

    def __enter__(self):
        self.end_ts = None
        self.start_ts = time.monotonic()
        base.send_slack(
            f"{self.start_emoji} start: {self.action}",
        )

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_ts = time.monotonic()

        if exc_value is None:
            emoji = self.end_emoji
            success_str = "success"
        else:
            emoji = self.fail_emoji
            success_str = "failed"
            # if exc_type is base.CmdException:
            #     attachments.append(
            #         {
            #             'blocks': [
            #                 {
            #                     'type': 'section',
            #                     'text': {
            #                         'type': 'plain_text',
            #                         'text': exc_value.node,
            #                         'emoji': True,
            #                     },
            #                 },
            #                 {
            #                     'type': 'section',
            #                     'text': {
            #                         'type': 'plain_text',
            #                         'text': exc_value.stderr or exc_value.stdout,
            #                         'emoji': True,
            #                     },
            #                 },
            #             ],
            #         }
            #     )

        base.send_slack(
            f"{emoji} {success_str}: {self.action} ({self.elapsed:.2f}s)",
        )


def run():
    with DeployMessenger("deploy"):
        print(
            base.cmd_n_raise2(
                "*",
                "state.sls",
                ["state.deploy"],
                tgt_type="compound",
            )
        )
