import logging


def write_log(msg):
    logging.basicConfig(
        level=logging.INFO, filename="logs.log",filemode="a+",
        format="%(asctime)s %(levelname)s %(message)s"
    )
    logging.info(msg)

def write_space():
    with open('logs.log', 'a+') as file:
        file.write("\n")