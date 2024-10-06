#!jinja|yaml
deploy jakdf:
    cmd.run:
        - runas: root
        - cwd: /opt/kaiju-number-eight
        - name: >-
            make git-pull-main && make deploy
        - failhard: True
