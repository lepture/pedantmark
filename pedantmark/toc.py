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
        elif level < parents[-1]:
            parents.pop()
            if parents and level <= parents[-1]:
                out += '</li>\n</ul>\n</li>\n<li>'
            else:
                parents.append(level)
                out += '</li>\n<li>'
        else:
            out += '</li>\n<li>'
        out += _render_item(text, index)
        index += 1

    return out + '</li>\n</ul>\n'


def _render_item(text, index):
    return '<a href="#toc-{}">{}</a>'.format(index, text.decode('utf-8'))
