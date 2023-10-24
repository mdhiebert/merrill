class Configuration:
    PDF_2062_FILEPATH = 'assets/2062_BLANK.pdf'
    PDF_1750_FILEPATH = 'assets/1750_BLANK.pdf'
    PDF_HAZDEC_FILEPATH = 'assets/HAZDEC_BLANK.pdf'

    # HAZDEC
    CEMA_HMO = ''
    SHIPPER_ADDRESS = CEMA_HMO + ''
    CONSIGNEE_INFORMATION = SHIPPER_ADDRESS
    AIRPORT_OF_DEPARTURE = ''
    DESTINATION_AIRPORT = ''
    EMERGENCY_CONTACT_INFO = ''
    ADDITIONAL_INFO = 'EMERGENCY CONTACT INFO: ' + EMERGENCY_CONTACT_INFO
    PLACE_OF_SIGNATURE = ''

CONFIG = Configuration()