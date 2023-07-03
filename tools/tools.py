import subprocess
import os
import yaml

config = ""
def load_config():
    global config
    if not config:
        with open("config.yaml", 'r') as f:
            config = yaml.safe_load(f)
    return config

class Command:

    def __init__(self, command, callback, strings_to_check, output_folder, output_file):
        self.command = command
        self.callback = callback
        self.strings_to_check = strings_to_check
        self.output_folder = output_folder
        self.output_file = output_file
        return

    def run_command(self):
        print(f"Now running: {self.command}")
        process = subprocess.Popen(
            ["sh", "-c", self.command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        if self.output_folder is not None and self.output_file is not None:
            os.makedirs(self.output_folder, exist_ok=True)

            output_file = os.path.join(self.output_folder, self.output_file)
            with open(output_file, 'w') as file:
                while True:
                    output = process.stdout.readline()
                    

                    if process.poll() is not None and output == '':
                        print(f"Done running: {self.command}")
                        break

                    if output:
                        file.write(output)  # Save output to file

                        if self.callback is not None:
                            for string in self.strings_to_check:
                                if string in output:
                                    self.callback(output.strip())

        return