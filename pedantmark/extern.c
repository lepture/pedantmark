#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "cmark-gfm.h"
#include "node.h"
#include "buffer.h"
#include "houdini.h"
#include "syntax_extension.h"
#include "extern.h"

static void h_escape_html0(cmark_strbuf *dest, const unsigned char *source,
                           size_t len, int secure) {
  houdini_escape_html0(dest, source, len, secure);
}

unsigned char *escape_html(const unsigned char *source, size_t len, int secure) {
  cmark_mem *mem = cmark_get_default_mem_allocator();
  cmark_strbuf buf = CMARK_BUF_INIT(mem);
  h_escape_html0(&buf, source, len, secure);
  unsigned char *data = buf.ptr;
  cmark_strbuf_free(&buf);
  return data;
}

const char *pedant_get_node_type(cmark_node *node) {
  if (node == NULL) {
    return "NONE";
  }

  if (node->extension && node->extension->get_type_string_func) {
    return node->extension->get_type_string_func(node->extension, node);
  }

  switch (node->type) {
  case CMARK_NODE_NONE:
    return "none";
  case CMARK_NODE_DOCUMENT:
    return "document";
  case CMARK_NODE_BLOCK_QUOTE:
    return "block_quote";
  case CMARK_NODE_LIST:
    return "list";
  case CMARK_NODE_ITEM:
    return "item";
  case CMARK_NODE_CODE_BLOCK:
    return "code_block";
  case CMARK_NODE_HTML_BLOCK:
    return "html_block";
  case CMARK_NODE_CUSTOM_BLOCK:
    return "custom_block";
  case CMARK_NODE_PARAGRAPH:
    return "paragraph";
  case CMARK_NODE_HEADING:
    return "heading";
  case CMARK_NODE_THEMATIC_BREAK:
    return "thematic_break";
  case CMARK_NODE_TEXT:
    return "text";
  case CMARK_NODE_SOFTBREAK:
    return "softbreak";
  case CMARK_NODE_LINEBREAK:
    return "linebreak";
  case CMARK_NODE_CODE:
    return "code";
  case CMARK_NODE_HTML_INLINE:
    return "html_inline";
  case CMARK_NODE_CUSTOM_INLINE:
    return "custom_inline";
  case CMARK_NODE_EMPH:
    return "emph";
  case CMARK_NODE_STRONG:
    return "strong";
  case CMARK_NODE_LINK:
    return "link";
  case CMARK_NODE_IMAGE:
    return "image";
  }

  return "_unknown";
}

struct render_state {
  cmark_strbuf *buf;
};

static int S_render_node(pedant_render_node_t cb, cmark_node *node,
                         cmark_event_type ev_type, struct render_state *state,
                         int options, void *userdata) {
  cmark_strbuf *buf = state->buf;
  bool entering = (ev_type == CMARK_EVENT_ENTER);
  // TODO: text
  cb(buf, node, entering, options, userdata);
  return 1;
}

char *cmark_render_pedant(pedant_render_node_t cb, cmark_node *root, int options, void *userdata) {
  char *result;

  cmark_strbuf buf = CMARK_BUF_INIT(cmark_node_mem(root));
  cmark_event_type ev_type;
  cmark_node *cur;

  struct render_state state = {&buf};

  cmark_iter *iter = cmark_iter_new(root);

  while ((ev_type = cmark_iter_next(iter)) != CMARK_EVENT_DONE) {
    cur = cmark_iter_get_node(iter);
    S_render_node(cb, cur, ev_type, &state, options, userdata);
  }
  result = (char *)cmark_strbuf_detach(&buf);

  cmark_iter_free(iter);
  return result;
}
