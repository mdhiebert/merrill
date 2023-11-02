""" class TxtOutput:

    def __init__(self, overall_description:str, admin_from:str, admin_to:str, packed_by:str):
        self.overall_description = overall_description
        self.admin_from = admin_from
        self.admin_to = admin_to
        self.packed_by = packed_by """

""" def fromForm(self):

    output = \
        'Admin Data:\n' \
        + 'OVERALL_DESCRIPTION: ' + self.overall_description + '\n' \
        + '2062_FROM: ' + self.admin_from + '\n' \
        + '2062_TO: ' + self.admin_to + '\n' \
        + '1750_PACKED_BY: ' + self.packed_by + '\n' \
        + '--------------------------------------------------------------------------------\n'
        
    allDB = equipmentTemp.query.order_by(equipmentTemp.UUID).all()
    print(allDB)
            
    with open('test_output/testoutput.txt', 'w+') as f:
        f.write('{}'.format(output))
        f.close

        def fromForm(self): """

def txtHeader(overall_description:str, admin_from:str, admin_to:str, packed_by:str):
    output = \
        'Admin Data:\n' \
        + 'OVERALL_DESCRIPTION: ' + overall_description + '\n' \
        + '2062_FROM: ' + admin_from + '\n' \
        + '2062_TO: ' + admin_to + '\n' \
        + '1750_PACKED_BY: ' + packed_by + '\n' \
        + '--------------------------------------------------------------------------------\n'
    return output

def txtBody(bodyInput):
    output = ''
    for x,y in bodyInput.items():
        for f in y.values():
            output = output + \
                str(f[0]) + 'x ' + \
                str(f[2]) + ' (' + \
                str(f[1]) + ')\n'
        if x != list(bodyInput.keys())[-1]: output = output + '#\n'
    return output

            
