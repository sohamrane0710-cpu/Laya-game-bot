
import json
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import vizdoom as vzd
from pynput import keyboard

from adapters.doom.state_adapter import DoomStateAdapter


OUTPUT_DIR = Path("data/demonstrations")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SESSION_ID = f"demo_{uuid.uuid4().hex[:10]}"
OUTPUT_FILE = OUTPUT_DIR / f"{SESSION_ID}.jsonl"

ACTION_FRAMES = 4

pressed_keys = set()
keys_lock = threading.Lock()
stop_event = threading.Event()

state_adapter = DoomStateAdapter()


def key_name(key):
    """Normalize keyboard keys into stable strings."""
    if key == keyboard.Key.space:
        return "space"

    if key == keyboard.Key.up:
        return "up"
    if key == keyboard.Key.left:
        return "left"
    if key == keyboard.Key.right:
        return "right"

    if hasattr(key, "char") and key.char:
        return key.char.lower()

    return str(key)


def on_press(key):
    name = key_name(key)

    if name == "esc":
        stop_event.set()
        return False

    with keys_lock:
        pressed_keys.add(name)


def on_release(key):
    name = key_name(key)

    with keys_lock:
        pressed_keys.discard(name)


def current_action():
    """Convert held keys into one supported DOOM action."""
    with keys_lock:
        keys = set(pressed_keys)

    forward = "w" in keys or "up" in keys
    left = "a" in keys or "left" in keys
    right = "d" in keys or "right" in keys
    attack = "space" in keys

    # Resolve conflicting left/right inputs.
    if left and right:
        left = right = False

    # Turning takes priority over forward movement.
    if left:
        return "left_attack" if attack else "turn_left"

    if right:
        return "right_attack" if attack else "turn_right"

    if forward:
        return "forward_attack" if attack else "forward"

    if attack:
        return "attack"

    return "wait"


def main():
    game = vzd.DoomGame()

    game.set_doom_scenario_path(
        vzd.scenarios_path + "/basic.wad"
    )
    game.set_doom_map("map01")
    game.set_screen_resolution(
        vzd.ScreenResolution.RES_640X480
    )
    game.set_screen_format(vzd.ScreenFormat.RGB24)
    game.set_window_visible(True)

    game.set_labels_buffer_enabled(True)
    game.set_objects_info_enabled(True)

    game.set_available_buttons([
        vzd.Button.MOVE_FORWARD,
        vzd.Button.TURN_LEFT,
        vzd.Button.TURN_RIGHT,
        vzd.Button.ATTACK,
    ])

    game.set_available_game_variables([
        vzd.GameVariable.HEALTH,
        vzd.GameVariable.AMMO2,
    ])

    game.set_episode_timeout(10000)
    game.init()
    game.new_episode()

    action_map = {
        "forward": [True, False, False, False],
        "turn_left": [False, True, False, False],
        "turn_right": [False, False, True, False],
        "attack": [False, False, False, True],
        "forward_attack": [True, False, False, True],
        "left_attack": [False, True, False, True],
        "right_attack": [False, False, True, True],
        "wait": [False, False, False, False],
    }

    step = 0

    try:
        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
        ) as listener:
            print("\nHuman demonstration recorder ready.")
            print("W / Up: move forward")
            print("A / Left: turn left")
            print("D / Right: turn right")
            print("Space: fire")
            print("Esc: stop recording")
            print(f"Saving to: {OUTPUT_FILE}")
            print("Focus the DOOM window and play.\n")

            with OUTPUT_FILE.open(
                "a", encoding="utf-8"
            ) as output:
                while (
                    not stop_event.is_set()
                    and not game.is_episode_finished()
                ):
                    raw_state = game.get_state()

                    if raw_state is None:
                        break

                    state = state_adapter.transform(raw_state)
                    action = current_action()

                    reward = game.make_action(
                        action_map[action],
                        ACTION_FRAMES,
                    )

                    terminal = game.is_episode_finished()
                    next_raw_state = (
                        None if terminal else game.get_state()
                    )
                    next_state = (
                        None
                        if next_raw_state is None
                        else state_adapter.transform(next_raw_state)
                    )

                    record = {
                        "session_id": SESSION_ID,
                        "step": step,
                        "timestamp": datetime.now(
                            timezone.utc
                        ).isoformat(),
                        "state": state,
                        "human_action": action,
                        "action_frames": ACTION_FRAMES,
                        "reward": float(reward),
                        "next_state": next_state,
                        "terminal": terminal,
                    }

                    output.write(
                        json.dumps(record) + "\n"
                    )
                    output.flush()

                    step += 1

                    if step % 25 == 0:
                        print(
                            f"Recorded {step} transitions | "
                            f"health={state['health']} | "
                            f"ammo={state['ammo']} | "
                            f"action={action}"
                        )

    finally:
        game.close()

    print(f"\nRecording finished: {step} transitions")
    print(f"Dataset: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
