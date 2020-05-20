import json


class Element:
    def __init__(self, i_id, i_type, tags):
        self.id = i_id
        self.type = i_type
        self.tags = {}
        if tags:
            for tag in tags:
                self.tags[tag['k']] = tag['v']

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.elem_id

    @property
    def elem_id(self):
        return self.type + '_' + str(self.id)
