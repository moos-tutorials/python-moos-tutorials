# Ping-Pong example with Active Queues

This is an example where the `ping.py` app sends a variable **PING** with the
value **Hello world!** and waits sets an active queue for a **PONG** variable.
The `pong.py` app count the number of incoming **PING** s and publishes it
under **PONG**.

## Usage
```shell
pAntler activequeue_pingpong.moos
```
