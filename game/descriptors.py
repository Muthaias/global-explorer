class ActionDescriptor:
    def __init__(
        self,
        title,
        type=None,
    ):
        self.title = title
        self.type = type


class NodeDescriptor:
    def __init__(
        self,
        title,
        description=None,
        type=None,
        background=None,
        title_image=None,
        id=None,
        position=None,
        parent=None,
        is_entry_point=False,
        tags=None,
    ):
        self.title = title
        self.description = description
        self.type = type
        self.background = background
        self.title_image = title_image
        self.id = id
        self.position = position
        self.parent = parent
        self.is_entry_point = is_entry_point
        self.tags = () if tags is None else tags
