def render_toc(toc):
    if not toc:
        return ''

    text, start_level = toc[0]
    out = '<ul>\n<li>' + _render_item(text, 1)
    parents = [start_level]

    index = 2
    for text, level in toc[1:]:
        if level > parents[-1]:
            out += '\n<ul>\n<li>'
            parents.append(level)
        elif level == parents[-1]:
            out += '</li>\n<li>'
        else:
            out = _outdent_item(out, parents, level)
        out += _render_item(text, index)
        index += 1

    return out + '</li>\n</ul>\n'


def _render_item(text, index):
    return '<a href="#toc-{}">{}</a>'.format(index, text.decode('utf-8'))


def _outdent_item(out, parents, level):
    parents.pop()
    if not parents or level > parents[-1]:
        parents.append(level)
        return out + '</li>\n<li>'
    elif level == parents[-1]:
        return out + '</li>\n</ul>\n</li>\n<li>'
    else:
        return _outdent_item(out + '</li>\n</ul>\n', parents, level)
