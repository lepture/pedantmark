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
    return "list_item";
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

const char *pedant_get_node_code_info(cmark_node *node) {
  return node->as.code.info.data;
}
const int pedant_get_node_heading_level(cmark_node *node) {
  return node->as.heading.level;
}
const bool pedant_get_node_list_bullet(cmark_node *node) {
  cmark_list_type list_type = node->as.list.list_type;
  return list_type == CMARK_BULLET_LIST;
}
const int pedant_get_node_list_start(cmark_node *node) {
  return node->as.list.start;
}
const char *pedant_get_node_link_url(cmark_node *node) {
  return node->as.link.url.data;
}
const char *pedant_get_node_link_title(cmark_node *node) {
  return node->as.link.title.data;
}

static char *S_flat_node(pedant_render_node_t cb, cmark_node *node,
                         int options, void *userdata) {

  cmark_strbuf buf = CMARK_BUF_INIT(cmark_node_mem(node));

  if (node->first_child) {
    cmark_node *next = node->first_child;
    while (next) {
      char *next_s = S_flat_node(cb, next, options, userdata);
      cmark_strbuf_puts(&buf, next_s);
      free(next_s);
      next = next->next;
    }
    const unsigned char *text = (const unsigned char *)cmark_strbuf_detach(&buf);
    cb(&buf, node, text, userdata);
  } else {
    switch (node->type) {
    case CMARK_NODE_CODE_BLOCK:
    case CMARK_NODE_TEXT:
    case CMARK_NODE_CODE:
      cb(&buf, node, escape_html(node->as.literal.data, node->as.literal.len, 0), userdata);
      break;

    case CMARK_NODE_HTML_BLOCK:
    case CMARK_NODE_HTML_INLINE:
      if (options & CMARK_OPT_UNSAFE) {
        cb(&buf, node, node->as.literal.data, userdata);
      } else {
        cb(&buf, node, escape_html(node->as.literal.data, node->as.literal.len, 0), userdata);
      }
      break;
    case CMARK_NODE_THEMATIC_BREAK:
    case CMARK_NODE_LINEBREAK:
      cb(&buf, node, (const unsigned char *)"", userdata);
      break;
    case CMARK_NODE_SOFTBREAK:
      if (options & CMARK_OPT_HARDBREAKS) {
        cb(&buf, node, (const unsigned char *)"br", userdata);
      } else if (options & CMARK_OPT_NOBREAKS) {
        cb(&buf, node, (const unsigned char *)" ", userdata);
      } else {
        cb(&buf, node, (const unsigned char *)"\n", userdata);
      }
      break;
    }
  }

  char *result = (char *)cmark_strbuf_detach(&buf);
  return result;
}

char *cmark_render_pedant(pedant_render_node_t cb, cmark_node *root,
                                   int options, void *userdata) {
  return S_flat_node(cb, root, options, userdata);
}
