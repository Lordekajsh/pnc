"""
Funções de gates.

As funções aqui retornam uma tupla contendo:
  O status (True, False, None).
  A gate que foi checada (Ruby_03, W4rlock, etc).
"""

import json
import random
import traceback
from json.decoder import JSONDecodeError
from typing import Optional, Tuple

import httpx

from utils import hc


class GateOffError(Exception):
    pass
  
async def semchk(card) -> Tuple[Optional[bool], str]:
    gate = "semchk"
    user, password = ("Ljzin", "juliaelucas12")
    print(f"[GATE_{gate}][{card}] Checking cc...")

    try:
        rt = await hc.get(
            "https://azkabancenter.online/azkabandev.php",
            params=dict(
                lista=card, usuario=user, senha=password, testador="2-preauth"
            ),
        )

        rjson = rt.json()
    except:
        return await semchk(card)

    print(f"[GATE_{gate}][{card}] {rjson}")

    rcode = (
        True
        if rjson.get("success") is True
        else True
        if rjson.get("success") is True
        else True
    )

    return rcode, semchk