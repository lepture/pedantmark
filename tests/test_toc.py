from pedantmark import MarkdownState, HTMLRenderer, markdown
from pedantmark.toc import render_toc

NORMAL_INDENT = '''
# a

## b

### c

#### d

# e
'''

NORMAL_HTML = '''
<ul>
<li><a href="#toc-1">a</a>
<ul>
<li><a href="#toc-2">b</a>
<ul>
<li><a href="#toc-3">c</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#toc-4">e</a></li>
</ul>
'''

MESS_INDENT = '''
## a

###### b

### c

#### d

# e
'''

MESS_HTML = '''
<ul>
<li><a href="#toc-1">a</a>
<ul>
<li><a href="#toc-2">b</a></li>
<li><a href="#toc-3">c</a>
<ul>
<li><a href="#toc-4">d</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#toc-5">e</a></li>
</ul>
'''


def test_normal_indent():
    state = MarkdownState(toc_level=3)
    html = markdown(NORMAL_INDENT, renderer=HTMLRenderer(), state=state)
    # h4 has no id
    assert '<h4>' in html
    toc = render_toc(state.toc)
    assert toc.strip() == NORMAL_HTML.strip()


def test_mess_indent():
    state = MarkdownState(toc_level=6)
    markdown(MESS_INDENT, renderer=HTMLRenderer(), state=state)
    toc = render_toc(state.toc)
    assert toc.strip() == MESS_HTML.strip()
