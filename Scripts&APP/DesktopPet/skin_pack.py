# -*- coding: utf-8 -*-

import json
from functools import lru_cache
from util import get_path

# 用于对皮肤包进行操作（如get_action_img）


@lru_cache(maxsize=128)
def get_action_img(pack: str, action: str) -> None:
    pass
