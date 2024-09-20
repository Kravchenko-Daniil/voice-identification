from hashlib import sha256
import base64
import os
import json
import pveagle
import pyfiglet
from pvrecorder import PvRecorder
from pystyle import Colorate, Colors
from datetime import datetime, timedelta
from pydub import AudioSegment
from animation import EnrollmentAnimation, FEEDBACK_TO_DESCRIPTIVE_MSG
from parameters import access_key, DEFAULT_DEVICE_INDEX
from rout import RoutToSite
from logs import write_log, write_space
from blockchain import Block, Blockchain


BANNER = pyfiglet.figlet_format("VOICE IDENTIFICATION")
console_pointer = Colorate.Horizontal(Colors.green_to_red, "[>] ")
input_pointer = Colorate.Horizontal(Colors.green_to_red, " : ")

blockchain = Blockchain()  # Создаем экземпляр блокчейна


# def add_audio_to_blockchain(name, data):
# print(f"Хэш аудиофайла добавлен в блокчейн: {data}")


def compare_voice(name):
    profiles = []
    speaker_labels = []

    with open("data.json") as f:
        chain = json.load(f)

    data = None
    for block in chain:
        if block["name"] == name:
            data = base64.b64decode(block["data"])
            break
    else:
        raise NameError

    profile = pveagle.EagleProfile.from_bytes(data)
    profiles.append(profile)

    try:
        eagle = pveagle.create_recognizer(
            access_key=access_key, speaker_profiles=profiles
        )
    except pveagle.EagleError as e:
        print(e)

    recognizer_recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX, frame_length=eagle.frame_length
    )
    # speaker_labels.append(os.path.splitext(os.path.basename(input_path))[0])
    recognizer_recorder.start()

    scores_list = []
    name_speaker = Colorate.Horizontal(Colors.blue_to_red, name)
    print(console_pointer + "Keep speaking until you see the result")

    time_start = datetime.now()
    while True:
        audio_frame = recognizer_recorder.read()
        scores = eagle.process(audio_frame)
        scores_list.append(scores[0])

        score = scores_list.count(1.0) >= 50
        write_log(
            f"{speaker_labels}: count={scores_list.count(1.0)}, len={len(scores_list)}"
        )
        if score:
            write_space()
            bool_result, text_result = (
                True,
                console_pointer + f"That's for sure you - {name_speaker}",
            )
            break
        else:
            if datetime.now() - time_start >= timedelta(seconds=6):
                write_space()
                bool_result, text_result = (
                    False,
                    console_pointer + f"That's for sure not {name_speaker}",
                )
                break

    recognizer_recorder.stop()
    recognizer_recorder.delete()
    eagle.delete()

    # Проверяем, есть ли хэш в блокчейне
    # if hmash_audio(input_path) in [block.data[0] for block in blockchain.chain]:
    #     print("Голос найден в блокчейне.")
    # else:
    #     print("Голос не найден в блокчейне.")

    return bool_result, text_result


def record_micro(name):
    try:
        eagle_profiler = pveagle.create_profiler(access_key=access_key)
    except pveagle.EagleError as e:
        print(e)

    enroll_recorder = PvRecorder(
        device_index=DEFAULT_DEVICE_INDEX,
        frame_length=eagle_profiler.min_enroll_samples,
    )
    phrase_example = Colorate.Horizontal(
        Colors.red_to_green, "Hello, my name is ... I confirm my identity."
    )
    print(
        console_pointer + "Keep speaking until the enrollment percentage reaches 100%"
    )
    print(
        console_pointer
        + f"Recording...\nSay something like{input_pointer} {phrase_example}"
    )

    enrollment_animation = EnrollmentAnimation()
    enrollment_animation.start()
    enroll_recorder.start()
    enroll_percentage = 0.0
    while enroll_percentage < 100.0:
        audio_frame = enroll_recorder.read()
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
        enrollment_animation.percentage = enroll_percentage
        enrollment_animation.feedback = " - %s" % FEEDBACK_TO_DESCRIPTIVE_MSG[feedback]

    enrollment_animation.stop()
    enroll_recorder.stop()
    speaker_profile = eagle_profiler.export()

    byts = speaker_profile.to_bytes()
    byts = base64.b64encode(byts).decode("utf-8")

    # new_block = Block(name=name, data=byts)
    blockchain.addBlock(name, byts)

    enroll_recorder.delete()


def mode_inputs():
    print(BANNER)
    mode_variants = Colorate.Horizontal(Colors.green_to_red, "record/compare/both")
    mode_color = Colorate.Horizontal(Colors.red_to_blue, "mode")
    mode = input(
        console_pointer + f"Choose {mode_color} {mode_variants}" + input_pointer
    )

    name = input(console_pointer + "What is your name?" + input_pointer)
    # path = f"voices/{name}.wav"

    if mode == "record":
        record_micro(name)
    elif mode == "compare":
        compare = compare_voice(name)
        print(compare[1])
        if compare[0]:
            RoutToSite().auth()
    elif mode == "both":
        record_micro(name)
        compare = compare_voice(name)
        print(compare[1])
        if compare[0]:
            RoutToSite().auth()


if __name__ == "__main__":
    mode_inputs()
