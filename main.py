import argparse
import shutil
import os
from merrill import Merrill

parser = argparse.ArgumentParser(
                    prog='merrill',
                    description='Automatically generates Army paperwork for equipment',
                    epilog='For any questions, refer to 1LT Hiebert')
parser.add_argument('working_directory', help = 'the target directory to work out of')

args = parser.parse_args()

output_directory = f'{args.working_directory}/paperwork'
equipment_list = f'{args.working_directory}/equipment.txt'

with open(equipment_list) as f:
    raw_text = f.read()

m = Merrill.from_text(raw_text)

try:
    shutil.rmtree(output_directory)
except Exception:
    pass

try:
    os.mkdir(output_directory)
except Exception:
    pass

m.generate_paperwork(output_directory = output_directory)