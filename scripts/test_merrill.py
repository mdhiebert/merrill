from merrill import Merill

with open('example.txt') as f:
    text = f.read()

m = Merill.from_text(text)

m.generate_paperwork()