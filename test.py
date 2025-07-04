"""
6.101 Lab:
Mice-sleeper
"""

#!/usr/bin/env python3
import os
import lab
import sys
import pickle
import doctest

import pytest

sys.setrecursionlimit(20000)

TEST_DIRECTORY = os.path.dirname(__file__)

TESTDOC_FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
TESTDOC_SKIP = ["lab"]


def test_all_doc_strings_exist():
    """Checking if docstrings have been written for everything in lab.py"""
    tests = doctest.DocTestFinder(exclude_empty=False).find(lab)
    for test in tests:
        if test.name in TESTDOC_SKIP:
            continue
        assert test.docstring, f"Oh no, '{test.name}' has no docstring!"


def test_newsmallgame():
    result = lab.new_game_2d(
        10,
        8,
        [
            (7, 3), (2, 6), (8, 7), (4, 4), (3, 5), (4, 6), (6, 2), (9, 4),
            (4, 2), (4, 0), (8, 6), (9, 7), (8, 5), (5, 0), (7, 2), (5, 3),
        ],
    )
    expected = {
        "board": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 2, "m", 1],
            [1, 2, 1, 2, 2, "m", 3, 2],
            ["m", 3, "m", 3, "m", 3, "m", 1],
            ["m", 4, 3, "m", 2, 2, 1, 1],
            [1, 3, "m", 4, 2, 0, 0, 0],
            [0, 2, "m", "m", 2, 2, 3, 2],
            [0, 1, 2, 3, 3, "m", "m", "m"],
            [0, 0, 0, 1, "m", 3, 4, "m"],
        ],
        "dimensions": (10, 8),
        "visible": [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
        ],
        "state": "ongoing",
    }
    for name in expected:
        assert result[name] == expected[name]


def test_newmediumgame():
    result = lab.new_game_2d(
        30,
        16,
        [
            (16, 6), (17, 7), (14, 4), (13, 4), (0, 7), (21, 6), (2, 5), (5, 5),
            (6, 10), (12, 6), (24, 14), (14, 1), (24, 1), (26, 12), (8, 15),
            (9, 3), (16, 0), (19, 13), (15, 14), (13, 10), (18, 10), (21, 15),
            (28, 15), (29, 14), (11, 15), (14, 8), (17, 8), (24, 8), (25, 5),
            (2, 1), (10, 3), (27, 2), (17, 6), (7, 15), (15, 0), (21, 8),
            (20, 0), (1, 10), (10, 4), (14, 6), (1, 0), (4, 11), (27, 0),
            (9, 13), (23, 5), (14, 12), (20, 15), (3, 15), (26, 14), (4, 8),
            (10, 15), (7, 11), (18, 1), (25, 4), (26, 3), (22, 14), (28, 2),
            (13, 2), (19, 6), (1, 4), (21, 4), (1, 9), (8, 7), (23, 1),
            (22, 11), (19, 5), (18, 7), (0, 6), (26, 4), (3, 4), (5, 9),
            (24, 13), (20, 8), (19, 0), (0, 3), (21, 13), (3, 3), (28, 9),
            (11, 1), (12, 10), (24, 10), (18, 13), (0, 0), (21, 0), (3, 13),
            (27, 13), (5, 15), (26, 9), (17, 4), (7, 9), (19, 9), (24, 7),
            (22, 5), (3, 8), (27, 8), (9, 5), (23, 13), (5, 2), (10, 2),
        ],
    )
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", "test2d_newmediumgame.pickle"
    )
    with open(exp_fname, "rb") as f:
        expected = pickle.load(f)
    for name in expected:
        assert result[name] == expected[name]


def test_newlargegame():
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", "test2d_newlargegame.pickle"
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", "test2d_newlargegame.pickle"
    )
    with open(exp_fname, "rb") as f:
        expected = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inputs = pickle.load(f)
    result = lab.new_game_2d(inputs["num_rows"], inputs["num_cols"], inputs["mice"])
    for name in expected:
        assert result[name] == expected[name]


def _do_test_2d_integration(test):
    """reveal, render, and render_2d_board on boards"""
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", f"test2d_integration_{test:02d}.pickle"
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", f"test2d_integration_{test:02d}.pickle"
    )
    with open(inp_fname, "rb") as f:
        inputs = pickle.load(f)
    with open(exp_fname, "rb") as f:
        expected = pickle.load(f)
    game = lab.new_game_2d(*inputs[0])
    moves_so_far = []
    for location, exp in zip(inputs[1], expected):
        moves_so_far.append(("d", location))
        num, g, render, renderx = exp
        reveal_res = lab.reveal_2d(game, *location)
        assert reveal_res == num, format_error_message(
            *inputs[0],
            moves_so_far,
            f"incorrect return value from reveal_2d: got {reveal_res!r} but expected {num!r}",
        )
        myrender = lab.render_2d(game, all_visible=False)
        assert myrender == render, (
            compare_renders(myrender, render, False)
            + "\n\n"
            + format_error_message(*inputs[0], moves_so_far, "")
        )
        myrender = lab.render_2d(game, all_visible=True)
        assert myrender == renderx, (
            compare_renders(render, renderx, True)
            + "\n\n"
            + format_error_message(*inputs[0], moves_so_far, "")
        )
        assert game["state"] == g["state"], format_error_message(
            *inputs[0],
            moves_so_far,
            f"incorrect state: got {game['state']!r} but expected {g['state']!r}",
        )

    last_state = game["state"]
    if last_state in {"won", "lost"}:
        for r in range(game["dimensions"][0]):
            for c in range(game["dimensions"][1]):
                assert lab.reveal_2d(game, r, c) == 0
                assert game["state"] == last_state
    else:
        for r in range(game["dimensions"][0]):
            for c in range(game["dimensions"][1]):
                if game["visible"][r][c]:
                    assert lab.reveal_2d(game, r, c) == 0
                    assert game["state"] == "ongoing"


def test_2d_integration():
    for testnum in range(9):
        _do_test_2d_integration(testnum)


def test_newsmall6dgame():
    """Testing new_game on a small 6-D board"""
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", "testnd_newsmall6dgame.pickle"
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", "testnd_newsmall6dgame.pickle"
    )
    with open(exp_fname, "rb") as f:
        expected = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inputs = pickle.load(f)
    result = lab.new_game_nd(inputs["dimensions"], inputs["mice"])
    for i in ("dimensions", "board", "visible", "state"):
        assert result[i] == expected[i]


def test_newlarge4dgame():
    """Testing new_game on a large 4-D board"""
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", "testnd_newlarge4dgame.pickle"
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", "testnd_newlarge4dgame.pickle"
    )
    with open(exp_fname, "rb") as f:
        expected = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inputs = pickle.load(f)
    result = lab.new_game_nd(inputs["dimensions"], inputs["mice"])
    for i in ("dimensions", "board", "visible", "state"):
        assert result[i] == expected[i]


def test_tiny_reveal_nd():
    # super tiny example 1D example
    F = False
    T = True
    game = lab.new_game_nd((4,), [(2,)])
    expected = {
        "dimensions": (4,),
        "state": "ongoing",
        "board": [0, 1, "m", 1],
        "visible": [F, F, F, F],
    }
    for i in ("dimensions", "board", "visible", "state"):
        assert game[i] == expected[i]

    assert lab.reveal_nd(game, (0,)) == 2
    assert game["visible"] == [T, T, F, F]
    assert game["state"] == "ongoing"

    assert lab.reveal_nd(game, (2,)) == 1
    assert game["visible"] == [T, T, T, F]
    assert game["state"] == "lost"

    # reset
    game = lab.new_game_nd((4,), [(2,)])
    assert lab.reveal_nd(game, (0,)) == 2
    assert game["visible"] == [T, T, F, F]
    assert game["state"] == "ongoing"

    assert lab.reveal_nd(game, (0,)) == 0
    assert game["visible"] == [T, T, F, F]
    assert game["state"] == "ongoing"

    assert lab.reveal_nd(game, (3,)) == 1
    assert game["visible"] == [T, T, F, T]
    assert game["state"] == "won"

    assert lab.reveal_nd(game, (2,)) == 0
    assert game["visible"] == [T, T, F, T]
    assert game["state"] == "won"

    # now test the reveal behavior on a small 1D game
    game = lab.new_game_nd((10,), [(0,), (7,), (2,)])
    expected = {
        "dimensions": (10,),
        "state": "ongoing",
        "board": ["m", 2, "m", 1, 0, 0, 1, "m", 1, 0],
        "visible": [F, F, F, F, F, F, F, F, F, F],
    }
    for i in ("dimensions", "board", "visible", "state"):
        assert game[i] == expected[i]

    # now let's reveal some squares!
    expected_vis = [F, F, F, T, T, T, T, F, F, F]
    assert lab.reveal_nd(game, (5,)) == 4
    assert game["visible"] == expected_vis
    for i in ("dimensions", "board", "state"):
        assert game[i] == expected[i]

    expected_vis = [F, T, F, T, T, T, T, F, F, F]
    assert lab.reveal_nd(game, (1,)) == 1
    assert game["visible"] == expected_vis
    for i in ("dimensions", "board", "state"):
        assert game[i] == expected[i]

    expected_vis = [F, T, F, T, T, T, T, F, T, F]
    assert lab.reveal_nd(game, (8,)) == 1
    assert game["visible"] == expected_vis
    for i in ("dimensions", "board", "state"):
        assert game[i] == expected[i]

    # reveal again
    for c in [1, 3, 4, 5, 6, 8]:
        assert lab.reveal_nd(game, (c,)) == 0
        assert game["visible"] == expected_vis
        for i in ("dimensions", "board", "state"):
            assert game[i] == expected[i]

    # win
    expected_vis = [F, T, F, T, T, T, T, F, T, T]
    assert lab.reveal_nd(game, (9,)) == 1
    assert game["visible"] == expected_vis
    assert game["state"] == "won"
    for i in ("dimensions", "board"):
        assert game[i] == expected[i]

    # reveal again
    for c in range(10):
        assert lab.reveal_nd(game, (c,)) == 0
        assert game["visible"] == expected_vis
        assert game["state"] == "won"
        for i in ("dimensions", "board"):
            assert game[i] == expected[i]

    #######################################################################
    # start over
    game = lab.new_game_nd((10,), [(0,), (7,), (2,)])
    for i in ("dimensions", "board", "visible", "state"):
        assert game[i] == expected[i]

    # lose
    expected_vis = [F, F, T, T, T, T, T, F, F, F]
    assert lab.reveal_nd(game, (4,)) == 4
    assert lab.reveal_nd(game, (2,)) == 1
    assert game["visible"] == expected_vis
    assert game["state"] == "lost"
    for i in ("dimensions", "board"):
        assert game[i] == expected[i]

    # reveal again
    for c in range(10):
        assert lab.reveal_nd(game, (c,)) == 0
        assert game["visible"] == expected_vis
        assert game["state"] == "lost"
        for i in ("dimensions", "board"):
            assert game[i] == expected[i]


@pytest.mark.parametrize("test", [1, 2, 3])
def test_nd_integration(test):
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", f"testnd_integration{test}.pickle"
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", f"testnd_integration{test}.pickle"
    )
    with open(exp_fname, "rb") as f:
        expected = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inputs = pickle.load(f)
    g = lab.new_game_nd(inputs["dimensions"], inputs["mice"])
    for location, results in zip(inputs["reveals"], expected):
        squares_revealed, game, rendered, rendered_all_visible = results
        res = lab.reveal_nd(g, location)
        assert res == squares_revealed
        for i in ("dimensions", "board", "visible", "state"):
            assert g[i] == game[i]
        assert lab.render_nd(g) == rendered
        assert lab.render_nd(g, True) == rendered_all_visible

    # reveal again
    res = lab.reveal_nd(g, location)
    assert res == 0
    for i in ("dimensions", "board", "visible", "state"):
        assert g[i] == game[i]
    assert lab.render_nd(g) == rendered
    assert lab.render_nd(g, True) == rendered_all_visible

    # lose
    if g["state"] == "ongoing":
        res = lab.reveal_nd(g, inputs["mice"][0])
        assert res == 1
        assert g["state"] == "lost"


@pytest.mark.parametrize("test", [1, 2, 3])
def test_safe_first_click_2d(test):
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", f"test2d_safe_first_click_{test:02d}.pickle"
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", f"test2d_safe_first_click_{test:02d}.pickle"
    )
    with open(exp_fname, "rb") as f:
        outputs = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inputs = pickle.load(f)
    for (game_params, reveals), output in zip(inputs, outputs):
        dims, mice = game_params
        nrows, ncols = dims
        game = lab.new_game_2d(nrows, ncols, mice)
        moves_so_far = []
        for location, exp in zip(reveals, output):
            num, g, render, renderx = exp
            moves_so_far.append(("d", location))
            reveal_res = lab.reveal_2d(game, *location)
            assert reveal_res == num, format_error_message(
                nrows,
                ncols,
                mice,
                moves_so_far,
                f"incorrect return value from reveal_2d: got {reveal_res!r} but expected {num!r}",
            )
            myrender = lab.render_2d(game, all_visible=False)
            assert myrender == render, (
                compare_renders(myrender, render, False)
                + "\n\n"
                + format_error_message(nrows, ncols, mice, moves_so_far, "")
            )
            myrender = lab.render_2d(game, all_visible=True)
            assert myrender == renderx, (
                compare_renders(render, renderx, True)
                + "\n\n"
                + format_error_message(nrows, ncols, mice, moves_so_far, "")
            )
            assert game["state"] == g["state"], format_error_message(
                nrows,
                ncols,
                mice,
                moves_so_far,
                f"incorrect state: got {game['state']!r} but expected {g['state']!r}",
            )


def test_safe_first_click_nd():
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", "testnd_safe_first_click.pickle"
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", "testnd_safe_first_click.pickle"
    )
    with open(exp_fname, "rb") as f:
        outputs = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inputs = pickle.load(f)
    for (game_params, reveals), output in zip(inputs, outputs):
        dims, mice = game_params
        game = lab.new_game_nd(dims, mice)
        for reveal, exp in zip(reveals, output):
            num, g, r, ra = exp
            assert (
                lab.reveal_nd(game, reveal) == num
            ), "number of revealed squares is incorrect"
            for key in g:
                assert game[key] == g[key], f"game['{key}'] does not match expected"
            assert lab.render_nd(game) == r, "render does not match expected"
            assert (
                lab.render_nd(game, all_visible=True) == ra
            ), "render with all_visible=True does not match expected"


def test_tiny_toggle_bed_2d():
    def toggle(game, coords):
        return lab.toggle_bed_2d(game, coords[0], coords[1])

    tiny_toggle_bed_tester(toggle, lab.render_2d)


def test_tiny_toggle_bed_nd():
    tiny_toggle_bed_tester(lab.toggle_bed_nd, lab.render_nd)


def tiny_toggle_bed_tester(toggle_func, render_func):
    exp = {"visible": [[False]], "dimensions": (1, 1), "state": "ongoing"}

    render_nobed = [["_"]]
    render_withbed = [["B"]]

    for (
        board,
        mouse_set,
    ) in [([[0]], set()), ([["m"]], {(0, 0)})]:
        g = lab.new_game_nd((1, 1), mouse_set)
        exp["board"] = board

        for i in range(10):
            res = toggle_func(g, (0, 0))
            for key in exp:
                assert g[key] == exp[key], f"Right-click should not modify game[{key}]"
            if i % 2 == 0:
                assert res, f"Bed should be toggled ON after {i+1} right click(s)"
                assert render_func(g) == render_withbed
            else:
                assert not res, f"Bed should be toggled OFF after {i+1} right click(s)"
                assert render_func(g) == render_nobed


def _test_bed_2d(test_number):
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", f"test_beds_2d_%02d.pickle" % test_number
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", f"test_beds_2d_%02d.pickle" % test_number
    )
    with open(exp_fname, "rb") as f:
        exp = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inp = pickle.load(f)

    nrows, ncols, mice, moves = inp
    mice = [tuple(i) for i in mice]
    game = lab.new_game_2d(nrows, ncols, mice)
    outputs, renders, full_renders, states = exp

    moves_so_far = []
    for i, move in enumerate(moves):
        move_type, coords = move
        moves_so_far.append(move)
        row, col = coords
        if move_type == "f":
            got = lab.toggle_bed_2d(game, row, col)
            exp = outputs[i]
            passed = got == exp
            msg = f"incorrect return value from toggle_bed_2d: got {got!r} but expected {exp!r}"
        else:
            got = lab.reveal_2d(game, row, col)
            exp = outputs[i]
            passed = got == exp
            msg = f"incorrect return value from reveal_2d: got {got!r} but expected {exp!r}"
        assert passed, format_error_message(nrows, ncols, mice, moves_so_far, msg)
        render = lab.render_2d(game, all_visible=False)
        assert render == renders[i], (
            compare_renders(render, renders[i], False)
            + "\n\n"
            + format_error_message(nrows, ncols, mice, moves_so_far, "")
        )
        render = lab.render_2d(game, all_visible=True)
        assert render == full_renders[i], (
            compare_renders(render, full_renders[i], True)
            + "\n\n"
            + format_error_message(nrows, ncols, mice, moves_so_far, "")
        )
        assert game["state"] == states[i], format_error_message(
            nrows,
            ncols,
            mice,
            moves_so_far,
            f"incorrect state: got {game['state']!r} but expected {states[i]!r}",
        )


def test_bed_2d():
    for testnum in range(1, 7):
        _test_bed_2d(testnum)


def test_bed_sfc_interactions():
    for testnum in range(8, 14):
        _test_bed_2d(testnum)


@pytest.mark.parametrize("test_number", range(10))
def test_full_integration(test_number):
    exp_fname = os.path.join(
        TEST_DIRECTORY, "test_outputs", f"full_integration_%02d.pickle" % test_number
    )
    inp_fname = os.path.join(
        TEST_DIRECTORY, "test_inputs", f"full_integration_%02d.pickle" % test_number
    )
    with open(exp_fname, "rb") as f:
        exp = pickle.load(f)
    with open(inp_fname, "rb") as f:
        inp = pickle.load(f)

    coords, mice, moves = inp
    game = lab.new_game_nd(coords, mice)
    outputs, renders, states = exp

    for i, move in enumerate(moves):
        move_type, coords = move
        if move_type == "f":
            assert lab.toggle_bed_nd(game, coords) == outputs[i]
        else:
            assert lab.reveal_nd(game, coords) == outputs[i]
        assert lab.render_nd(game, all_visible=False) == renders[i]
        assert game["state"] == states[i]


def compare_renders(got, expected, full=False):
    out = []
    if len(got) != len(expected) or not all(
        len(i) == len(j) for i, j in zip(got, expected)
    ):
        out.append("incorrect length of rendered output!")
    for r, erow in enumerate(expected):
        for c, exp in enumerate(erow):
            try:
                sub = got[r][c]
            except:
                continue
            if sub != exp:
                out.append(
                    f"incorrect value at ({r},{c}): got {sub!r} but expected {exp!r}"
                )
    if out:
        return (
            f"your result for render_2d(game, all_visible={full}) produced incorrect results:\n\n"
            + "\n".join(out)
        )


def format_error_message(nrows, ncols, mice, moves_so_far, phrase=None):
    output = [phrase] if phrase else []
    output.extend(
        [
            "\nthe following code was run before the test case failed.",
            "the last call in this sequence was the one that caused the error.",
            "you can test this sequence of moves in the web ui or directly in code.\n",
        ]
    )
    output.append(f"game = new_game_2d({nrows}, {ncols}, {mice})")
    for m, loc in moves_so_far:
        output.append(
            f"{'reveal_2d' if m == 'd' else 'toggle_bed_2d'}(game, {loc[0]}, {loc[1]})"
        )
    return "\n" + "\n".join(output) + "\n\n"
