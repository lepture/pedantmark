// cmark-gfm.h
typedef enum {
  CMARK_NODE_NONE = ...
} cmark_node_type;

typedef struct cmark_node cmark_node;
typedef struct cmark_parser cmark_parser;

typedef struct cmark_mem {
  void *(*calloc)(size_t, size_t);
  void *(*realloc)(void *, size_t);
  void (*free)(void *);
} cmark_mem;

typedef void (*cmark_free_func) (cmark_mem *mem, void *user_data);

typedef struct _cmark_llist
{
  struct _cmark_llist *next;
  void         *data;
} cmark_llist;

cmark_llist * cmark_llist_append    (cmark_mem         * mem,
                                     cmark_llist       * head,
                                     void              * data);

void          cmark_llist_free_full (cmark_mem         * mem,
                                     cmark_llist       * head,
                                     cmark_free_func     free_func);

void          cmark_llist_free      (cmark_mem         * mem,
                                     cmark_llist       * head);

const char *cmark_version_string();

char *cmark_markdown_to_html(const char *text, size_t len, int options);
cmark_node *cmark_parse_document(const char *buffer, size_t len, int options);
cmark_node_type cmark_node_get_type(cmark_node *node);

char *cmark_render_xml(cmark_node *root, int options);
char *cmark_render_html(cmark_node *root, int options, cmark_llist *extensions);
char *cmark_render_man(cmark_node *root, int options, int width);
char *cmark_render_commonmark(cmark_node *root, int options, int width);
char *cmark_render_plaintext(cmark_node *root, int options, int width);
char *cmark_render_latex(cmark_node *root, int options, int width);

cmark_parser *cmark_parser_new(int options);
void cmark_parser_free(cmark_parser *parser);
void cmark_parser_feed(cmark_parser *parser, const char *buffer, size_t len);
cmark_node *cmark_parser_finish(cmark_parser *parser);

#define CMARK_OPT_DEFAULT 0
#define CMARK_OPT_SOURCEPOS ...
#define CMARK_OPT_HARDBREAKS ...
#define CMARK_OPT_NOBREAKS ...
#define CMARK_OPT_VALIDATE_UTF8 ...
#define CMARK_OPT_SMART ...
#define CMARK_OPT_GITHUB_PRE_LANG ...
#define CMARK_OPT_LIBERAL_HTML_TAG ...
#define CMARK_OPT_FOOTNOTES ...
#define CMARK_OPT_STRIKETHROUGH_DOUBLE_TILDE ...
#define CMARK_OPT_TABLE_PREFER_STYLE_ATTRIBUTES ...
#define CMARK_OPT_FULL_INFO_STRING ...
#define CMARK_OPT_UNSAFE ...

typedef struct cmark_syntax_extension cmark_syntax_extension;

// buffer.h
typedef int32_t bufsize_t;
typedef struct {
  cmark_mem *mem;
  unsigned char *ptr;
  bufsize_t asize, size;
} cmark_strbuf;
void cmark_strbuf_puts(cmark_strbuf *buf, const char *string);

// cmark-gfm-extension_api.h
cmark_syntax_extension *cmark_find_syntax_extension(const char *name);
int cmark_parser_attach_syntax_extension(cmark_parser *parser, cmark_syntax_extension *extension);
cmark_llist *cmark_parser_get_syntax_extensions(cmark_parser *parser);


// extensions/cmark-gfm-core-extensions.h
void cmark_gfm_core_extensions_ensure_registered(void);
