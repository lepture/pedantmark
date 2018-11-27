#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "cmark-gfm.h"
#include "node.h"
#include "buffer.h"
#include "houdini.h"
#include "syntax_extension.h"
#include "scanners.h"
#include "cmark-gfm-core-extensions.h"
#include "extern.h"

unsigned char *escape_html(const unsigned char *source, size_t len, int secure) {
  cmark_mem *mem = cmark_get_default_mem_allocator();
  cmark_strbuf buf = CMARK_BUF_INIT(mem);
  houdini_escape_html0(&buf, source, len, secure);
  unsigned char *data = buf.ptr;
  cmark_strbuf_free(&buf);
  return data;
}

unsigned char *escape_href(const unsigned char *source, size_t len) {
  cmark_mem *mem = cmark_get_default_mem_allocator();
  cmark_strbuf buf = CMARK_BUF_INIT(mem);
  houdini_escape_href(&buf, source, len);
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
  case CMARK_NODE_FOOTNOTE_REFERENCE:
    return "footnote_ref";
  case CMARK_NODE_FOOTNOTE_DEFINITION:
    return "footnote_def";
  }

  return "_unknown";
}

const char *pedant_get_node_code_info(cmark_node *node) {
  return (const char *)node->as.code.info.data;
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
  return (const char *)node->as.link.url.data;
}
const char *pedant_get_node_link_title(cmark_node *node) {
  return (const char *)escape_html(node->as.link.title.data, node->as.link.title.len, 0);
}
const bool pedant_get_node_paragraph_tight(cmark_node *node) {
  cmark_node *parent = cmark_node_parent(node);
  cmark_node *grandparent = cmark_node_parent(parent);
  if (grandparent != NULL && grandparent->type == CMARK_NODE_LIST) {
    return grandparent->as.list.tight;
  } else {
    return false;
  }
}
const char *pedant_get_node_table_cell_info(cmark_node *node) {
  static char buffer[3];
  bool is_head = cmark_gfm_extensions_get_table_row_is_header(node->parent);
  uint8_t *alignments = cmark_gfm_extensions_get_table_alignments(node->parent->parent);

  if (is_head) {
    buffer[0] = 'h';
  } else {
    buffer[0] = 'd';
  }

  cmark_node *n;
  int i = 0;
  for (n = node->parent->first_child; n; n = n->next, ++i)
    if (n == node)
      break;

  buffer[1] = alignments[i];
  buffer[2] = '\0';
  return buffer;
}

static int S_plain_node(cmark_strbuf *buf, cmark_node *node) {
  if (node->first_child) {
    cmark_node *next = node->first_child;
    while (next) {
      S_plain_node(buf, next);
      next = next->next;
    }
  } else {
    switch (node->type) {
    case CMARK_NODE_TEXT:
    case CMARK_NODE_CODE:
    case CMARK_NODE_HTML_INLINE:
      houdini_escape_html0(buf, node->as.literal.data, node->as.literal.len, 0);
      break;
    case CMARK_NODE_LINEBREAK:
    case CMARK_NODE_SOFTBREAK:
      cmark_strbuf_putc(buf, ' ');
      break;
    }
    return 1;
  }
  return 1;
}

static char *S_flat_node(pedant_render_node_t cb, cmark_node *node, int options,
                         bool render_plain, void *userdata) {

  cmark_strbuf buf = CMARK_BUF_INIT(cmark_node_mem(node));

  if (render_plain) {
    S_plain_node(&buf, node);
    return (char *)cmark_strbuf_detach(&buf);
  }

  char *flat_s;

  switch (node->type) {
  case CMARK_NODE_CODE:
  case CMARK_NODE_TEXT:
    cb(&buf, node, escape_html(node->as.literal.data, node->as.literal.len, 0), userdata);
    break;
  case CMARK_NODE_CODE_BLOCK:
    cb(&buf, node, escape_html(node->as.code.literal.data, node->as.code.literal.len, 0), userdata);
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
  case CMARK_NODE_SOFTBREAK:
    cb(&buf, node, (const unsigned char *)"", userdata);
    break;
  case CMARK_NODE_FOOTNOTE_REFERENCE:
    cb(&buf, node, node->as.literal.data, userdata);
    break;
  default:
    if (node->first_child) {
      bool next_plain = node->type == CMARK_NODE_IMAGE;
      cmark_node *next = node->first_child;
      while (next) {
        flat_s = S_flat_node(cb, next, options, next_plain, userdata);
        cmark_strbuf_puts(&buf, flat_s);
        free(flat_s);
        next = next->next;
      }
      const unsigned char *text = (const unsigned char *)cmark_strbuf_detach(&buf);
      cb(&buf, node, text, userdata);
    }
  }

  return (char *)cmark_strbuf_detach(&buf);
}

char *cmark_render_pedant(pedant_render_node_t cb, cmark_node *root,
                          int options, void *userdata) {
  return S_flat_node(cb, root, options, 0, userdata);
}
