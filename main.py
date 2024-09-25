#!/usr/bin/env python3.8

import logging
import time
import asyncio

import requests
import nio


async def sendmsg(msg) -> None:
    client = nio.AsyncClient("https://matrix.org", "@d33tah-bot1:matrix.org")

    await client.login(open('haslo.txt').read().strip())

    result = await client.room_send(
        room_id=open('room_id.txt').read().strip(),
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": msg,
        }
    )
    logging.info('sent notification(msg=%r) => %s', msg, result)


def notify(msg):
    asyncio.get_event_loop().run_until_complete(sendmsg(msg))


def isitopen():
    return bool(
        len(
            requests.get(
                "https://at.hs-ldz.pl/api/v1/users?online=true"
            ).json()
        )
    )


def is_status_stable(nowisopen, num_checks):
    for i in range(num_checks):
        if isitopen() != nowisopen:
            return False
        time.sleep(60)
    return True


def main():
    isopen = False
    while True:
        time.sleep(60)
        nowisopen = isitopen()
        logging.debug('nowisopen=%s, isopen=%s', nowisopen, isopen)
        if nowisopen and not isopen:
            if is_status_stable(nowisopen, num_checks=1):
                notify("Spejs jest otwarty! Więcej info: https://at.hs-ldz.pl")
                isopen = nowisopen
        elif isopen and not nowisopen:
            if is_status_stable(nowisopen, num_checks=15):
                notify(
                    "Spejs jest zamknięty! Więcej info: https://at.hs-ldz.pl"
                )
                isopen = nowisopen


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
