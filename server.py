#!/usr/bin/env python3

"""
6.1010 Mice-sleeper Game Server
"""

import os
import sys
import html
import json
import random
import importlib
import mimetypes
import traceback

from wsgiref.simple_server import make_server

import lab


LOCATION = os.path.realpath(os.path.dirname(__file__))
CURRENT_GAME = None

sys.setrecursionlimit(100000)


def parse_post(environ):
    try:
        body_size = int(environ.get("CONTENT_LENGTH", 0))
    except:
        body_size = 0

    body = environ["wsgi.input"].read(body_size)
    try:
        return json.loads(body)
    except:
        return {}


def new_game(params):
    global CURRENT_GAME
    print("[reloading lab.py in case you changed something]")
    importlib.reload(lab)
    if isinstance(params["mice"], int):
        all_cells = [
            (r, c) for r in range(params["rows"]) for c in range(params["cols"])
        ]
        random.shuffle(all_cells)
        params["mice"] = all_cells[: params["mice"]]
    CURRENT_GAME = lab.new_game_2d(
        params["rows"], params["cols"], [tuple(i) for i in params["mice"]]
    )
    return {
        "render": lab.render_2d(CURRENT_GAME, all_visible=False),
        "render_full": lab.render_2d(CURRENT_GAME, all_visible=True),
        "mice": [list(b) for b in params["mice"]],
    }


def new_game_nd(params):
    global CURRENT_GAME
    print("[reloading lab.py in case you changed something]")
    importlib.reload(lab)
    if isinstance(params["mice"], int):
        rand = lab.random_coordinates(
            params["dimensions"] + [random.randint(1, 61016101)]
        )
        mice = set()
        while len(mice) < params["mice"]:
            mice.add(next(rand))
        params["mice"] = mice
    CURRENT_GAME = lab.new_game_nd(
        params["dimensions"], [tuple(i[:-1]) for i in params["mice"]]
    )
    return {
        "render": lab.render_nd(CURRENT_GAME, all_visible=False),
        "render_full": lab.render_nd(CURRENT_GAME, all_visible=True),
        "mice": [list(b) for b in params["mice"]],
    }


def reveal(params):
    location = params["row"], params["col"]
    num = lab.reveal_2d(CURRENT_GAME, params["row"], params["col"])
    return {
        "revealed": list(location),
        "count": num,
        "state": CURRENT_GAME["state"],
        "render": lab.render_2d(
            CURRENT_GAME, all_visible=CURRENT_GAME["state"] != "ongoing"
        ),
        "render_full": lab.render_2d(CURRENT_GAME, all_visible=True),
    }


def reveal_nd(params):
    location = tuple(params["coords"])
    num = lab.reveal_nd(CURRENT_GAME, location)
    return {
        "revealed": list(location),
        "count": num,
        "state": CURRENT_GAME["state"],
        "render": lab.render_nd(
            CURRENT_GAME, all_visible=CURRENT_GAME["state"] != "ongoing"
        ),
        "render_full": lab.render_nd(CURRENT_GAME, all_visible=True),
    }


def bed(params):
    result = lab.toggle_bed_2d(CURRENT_GAME, params["row"], params["col"])
    return {
        "render": lab.render_2d(CURRENT_GAME),
        "render_full": lab.render_2d(CURRENT_GAME, all_visible=True),
        "bed": result,
    }


def bed_nd(params):
    result = lab.toggle_bed_nd(CURRENT_GAME, tuple(params["coords"]))
    return {
        "render": lab.render_nd(CURRENT_GAME),
        "render_full": lab.render_nd(CURRENT_GAME, all_visible=True),
        "bed": result,
    }


funcs = {
    "new_game": new_game,
    "reveal": reveal,
    "bed": bed,
    "new_game_nd": new_game_nd,
    "reveal_nd": reveal_nd,
    "bed_nd": bed_nd,
}


def application(environ, start_response):
    custom_headers = []
    path = (environ.get("PATH_INFO", "") or "").lstrip("/")
    
    if path in funcs:
        try:
            out = funcs[path](parse_post(environ))
            body = json.dumps(out).encode("utf-8")
            status = "200 OK"
            type_ = "application/json"
        except Exception:
            tb = traceback.format_exc()
            print(
                "--- Python error (likely in your lab code) during the next operation:\n"
                + tb,
                end="",
            )
            status = "200 OK"
            type_ = "application/json"
            body = json.dumps({"error": tb}).encode("utf-8")
    elif path == "":
        path = "index.html"

    if path not in funcs:
        static_file = path
        if static_file.startswith("ui/"):
            static_file = static_file[3:]
        test_fname = os.path.join(LOCATION, "ui", static_file)
        try:
            status = "200 OK"
            with open(test_fname, "rb") as f:
                body = f.read()
            type_ = mimetypes.guess_type(test_fname)[0] or "text/plain"
        except FileNotFoundError:
            status = "404 FILE NOT FOUND"
            body = test_fname.encode("utf-8")
            type_ = "text/plain"

    len_ = str(len(body))
    headers = [("Content-type", type_), ("Content-length", len_), *custom_headers]
    start_response(status, headers)
    return [body]


if __name__ == "__main__":
    try:
        lab.new_game_nd((5, 5), [])
        nd_ready = True
    except:
        nd_ready = False

    PORT = 6101
    print(f"starting server.")
    print(f"navigate to http://localhost:{PORT}/ to choose game mode.")
    print(f"- or go directly to /2d.html or /nd.html")
    with make_server("", PORT, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
