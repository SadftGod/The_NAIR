from modules.server_exceptions import RubberException


class DefaultValidator:
    def __init__(self):
        pass

    @staticmethod
    def validate_id(*ids):
        for id in ids:
            if not isinstance(id,int):
                RubberException.fastRubber("Id must be integer type!",3)

            if id < 0:
                RubberException.fastRubber("ID must be greater than zero", 3)

            