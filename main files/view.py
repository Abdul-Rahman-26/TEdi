import logging

# Set up a logger with the same name and file as used in the previous code
logger = logging.getLogger('user_input_logger')
handler = logging.FileHandler('user_input.log')
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# Read and print the contents of the log file
with open('user_input.log', 'r') as f:
    for line in f:
        print(line.strip())
