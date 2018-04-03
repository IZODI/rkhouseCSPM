# rkhousCSPM

## Crowd-Sourced PokeMap for RocketMap

- Install discord.py using: python3 -m pip install -U discord.py
- Set up config.py
- Run with: python3 rkhouscspm.py

- You may need `pip3 install mysqlclient`


- Note: Gym names in raids do not have to be completely filled in, just enough so MySQL can find a single gym.

## Commands

    ^gym -- show gyms like name provided, also a way to know if they are in the db
    ^raid -- input raid into database so that it shows on map for all to see
    ^example -- shows an example of an input
    ^commands -- shows the commands
    ^raidcp -- show the raid cp of specified mon
    ^spawn -- adds spawn of specified pokemon to map. Timer set to 15 minutes as it is unknown.


- Mine does not currently do built in raid notifiers sent to discord as an embed. It is currently being worked on on notifier branch.


[Use with NovaBot to get updates to channels of things you report](https://github.com/novskey/novabot/tree/wip)


## Made by @rkhous#1447

[CSPM For Monocle](https://github.com/rkhous/CSPM)


[Support The Build!](https://www.paypal.me/zod5578)


[ZOD's Discord for help... maybe](https://discord.gg/jNPzJKT)
