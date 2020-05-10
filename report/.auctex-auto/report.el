(TeX-add-style-hook
 "report"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-environments-local "python")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "url")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "inputenc"
    "amsmath"
    "amsthm"
    "amssymb"
    "calrsfs"
    "wasysym"
    "verbatim"
    "bbm"
    "color"
    "graphics"
    "geometry"
    "graphicx"
    "url"
    "esvect"
    "mathtools"
    "bm"
    "latexsym"
    "mathrsfs"
    "amsfonts"
    "enumitem"
    "xcolor"
    "textcomp"
    "float"
    "nccmath"
    "dirtree"
    "hyperref"
    "listings")
   (TeX-add-symbols
    '("numberstyle" 1))
   (LaTeX-add-labels
    "fig:raw"
    "fig:initial_process"
    "fig:er"
    "fig:schema"
    "fig:datatable"
    "fig:iterative_explorer"
    "fig:review_length"
    "fig:rank"
    "fig:annual"
    "lst:query1"
    "lst:query2")
   (LaTeX-add-environments
    "faq")
   (LaTeX-add-bibliographies)
   (LaTeX-add-xcolor-definecolors
    "codegreen"
    "codegray"
    "codepurple"
    "backcolour"
    "bookColor"
    "deepblue"
    "deepred"
    "deepgreen")
   (LaTeX-add-listings-lstdefinestyles
    "mystyle"))
 :latex)

