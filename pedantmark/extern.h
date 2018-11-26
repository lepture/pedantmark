#include "buffer.h"

unsigned char *escape_html(const unsigned char *source, size_t length, int secure);
unsigned char *escape_href(const unsigned char *source, size_t len);

typedef void (*pedant_render_node_t)(cmark_strbuf *buf, cmark_node *node, const unsigned char *text, void *userdata);
char *cmark_render_pedant(pedant_render_node_t cb, cmark_node *root, int options, void *userdata);

const char *pedant_get_node_type(cmark_node *node);
const char *pedant_get_node_code_info(cmark_node *node);
const int pedant_get_node_heading_level(cmark_node *node);
const bool pedant_get_node_list_bullet(cmark_node *node);
const int pedant_get_node_list_start(cmark_node *node);
const char *pedant_get_node_link_url(cmark_node *node);
const char *pedant_get_node_link_title(cmark_node *node);
const bool pedant_get_node_paragraph_tight(cmark_node *node);
const char *pedant_get_node_table_cell_info(cmark_node *node);
