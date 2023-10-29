class TxtOutput:

    def __init__(self, overall_description:str, admin_from:str, admin_to:str, packed_by:str, items ):
        self.overall_description = overall_description
        self.admin_from = admin_from
        self.admin_to = admin_to
        self.packed_by = packed_by
        self.items = items

    def fromForm(self):

        output = \
            'Admin Data:\n' \
            + 'OVERALL_DESCRIPTION: ' + self.overall_description + '\n' \
            + '2062_FROM: ' + self.admin_from + '\n' \
            + '2062_TO: ' + self.admin_to + '\n' \
            + '1750_PACKED_BY: ' + self.packed_by + '\n' \
            + '--------------------------------------------------------------------------------\n'
        
        for x in self.items:
            i = self.items[x]
            q = i[0]
            d = i[1]
            s = i[2]
            output = output + \
                q + 'x ' + d + ' (' + s + ')\n'
            
        with open('test_output/testoutput.txt', 'w+') as f:
            f.write('{}'.format(output))
            f.close
        