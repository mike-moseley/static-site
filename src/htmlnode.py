# Thanks Boots
VOID_TAGS = {"img", "link"}

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
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None and self.tag not in VOID_TAGS:
            raise ValueError("Leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        string = ""
        match self.tag:
            case "p" | "b" | "i" | "div" | "span" |\
                "h1" | "h2" | "h3" | "h4" | "h5" | "h6"\
                "li" | "code" | "pre":
                string = f'<{self.tag}>{self.value}</{self.tag}>'
            case "a":
                href = ""
                if self.props is not None:
                    href = self.props["href"]
                string = f'<{self.tag} href="{href}">{self.value}</{self.tag}>'
            case "img":
                if self.props is not None:
                    src = self.props.get("src") if self.props else ""
                    alt = self.props.get("alt") if self.props else ""
                string = f'<{self.tag} src="{src}" alt="{alt}">'
        return string

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("Parent nodes must have children.")
        if not isinstance(self.children, list):
            raise ValueError("Children must be a list.")

        html = f"<{self.tag}>"
        for c in self.children:
            if c is str:
                html += c
            else:
                html += f'{c.to_html()}'
        html += f"</{self.tag}>"
        return html

