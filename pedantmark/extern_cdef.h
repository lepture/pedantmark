unsigned char *escape_html(const unsigned char *source, size_t length, int secure);

typedef void (*pedant_render_node_t)(cmark_strbuf *buf, cmark_node *node, const unsigned char *text, void *userdata);
char *cmark_render_pedant(pedant_render_node_t cb, cmark_node *root, int options, void *userdata);

const char *pedant_get_node_type(cmark_node *node);
extern "Python" void pedant_render_node(cmark_strbuf *, cmark_node *, const unsigned char *, void *);
