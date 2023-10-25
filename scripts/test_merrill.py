from merrill import Merrill

with open('example.txt') as f:
    text = f.read()

m = Merrill.from_text(text)

m.generate_paperwork()