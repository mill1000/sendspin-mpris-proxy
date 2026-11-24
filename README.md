# sendspin-mpris-proxy

Proxy sendspin-cpp-cli event hooks to the MPRIS D-Bus interface.

Primarily intended to integrate with [mpris-monitor](https://github.com/mill1000/mpris-monitor).

## Install
Instructions are for a Raspberry Pi running Debian Trixie. Adjust as necessary.

- Install globally via pipx
```
sudo pipx install --global .
```

- Copy DBus policy: 
```
sudo cp sendspin-mpris-proxy-policy.conf /etc/dbus-1/system.d
```

- Copy systemd service:
```
sudo cp sendspin-mpris-proxy.service /etc/systemd/system
```

- Reload systemd:
```
sudo systemctl daemon-reload
```

- Enable and start proxy service:
```
sudo systemctl enable --now sendspin-mpris-proxy.service
```

- Configure sendspin-cpp-cli hooks in `/etc/sendspin-cli.conf`:
```
hook-start = /usr/local/bin/sendspin-on-event
hook-stop = /usr/local/bin/sendspin-on-event
```