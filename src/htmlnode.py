class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = ''
        if self.props is None:
            return ''
        else:
            for p in self.props:
                html += f' {p}={self.props[p]}'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        tag_bool = self.tag == other.tag
        value_bool = self.value == other.value
        children_bool = self.children == other.children
        prop_bool = self.props == other.props

        return tag_bool and value_bool and children_bool and prop_bool
