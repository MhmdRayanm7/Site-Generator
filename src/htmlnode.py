
class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        text = ""
        for key, value in self.props.items():
            text += f' {key}="{value}"'
        return text

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        ) 

class LeafNode(HTMLNode):
    def __init__(self, tag, value):
        super().__init__(tag, value, children=None, props=None)

    def to_html(self)-> str :
        if self.value is None:
            raise ValueError("there is no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (
            f"LeafNode(tag={self.tag!r}, value={self.value!r}, "
            f"props={self.props!r})"
        )


