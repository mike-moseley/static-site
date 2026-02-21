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

class LeafNode(HTMLNode):
    def __init__(self, value, tag, props=None):
        super().__init__(value, tag, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        string = ""
        match self.tag:
            case "p" | "b" | "i" | "div":
                string = f'<{self.tag}>{self.value}</{self.tag}>'
            case "a":
                href = ""
                if self.props is not None:
                    href = self.props["href"]
                string = f'<{self.tag} href="{href}">{self.value}</{self.tag}>'
            case "img":
                src = ""
                if self.props is not None:
                    src = self.props["src"]
                string = f'<{self.tag} src="{src}" alt="{self.value}">'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
