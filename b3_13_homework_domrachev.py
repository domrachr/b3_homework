import sys

class Tag(object):
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.is_single = is_single
        self.attributes = {}
        if klass is not None:
            self.attributes["class"] = " ".join(klass)        
        for attr, value in kwargs.items():
            self.attributes[attr] = value
        self.children = []
        
    def __add__(self,other):
        # Сложение для класса Tag по сути - просто добавление второго слагаемого в список подчиненных тэгов
        self.children.append(other)
        return self
        
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s\n" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)

            else:
                return "<{tag} {attrs}>{text}</{tag}>\n".format(tag=self.tag, attrs=attrs, text=self.text)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return str(self)

class TopLevelTag(Tag):
    def __init__(self, tag, klass=None, **kwargs):
        # TopLevelTag - всегда парный
        super().__init__(tag=tag, is_single=False, klass=klass, **kwargs)

class HTML(Tag):
    def __init__(self, output=None, klass=None, **kwargs):
        self.output = output
        super().__init__(tag="html", klass=klass, **kwargs)

    def __exit__(self, type, value, traceback):
        if self.output:
            # Вывести в файл
            with open(output,"w",encoding="UTF-8") as f:
                f.write(str(self))
        else:
            # Вывести на экран
            print(self)

# Если программу запустить без параметров - выведет результат на экран. Если же указать параметром имя файла - программа запишет код в этот файл
if __name__ == "__main__":
    if len(sys.argv) > 1:
        output=sys.argv[1]
    else:
        output = None
    with HTML(output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body