#!/usr/bin/env python3

import os
import string

OUTPUT_DIR = '_wheels'
os.makedirs(OUTPUT_DIR, exist_ok=True)


tmpl = string.Template(r"""\documentclass{standalone}

\usepackage[usenames,dvipsnames]{xcolor}
\usepackage{tikz}

\definecolor{DarkBlue}{HTML}{5c5c5c}
\definecolor{AlexRed}{HTML}{C7301F}

\begin{document}
  \begin{tikzpicture}
    %\fill [white] (0, 0) circle (6);
    \draw [$color, line width=7pt] (0, 0) circle (5);
    \foreach \s in {1, ..., $camsize} {
      \draw [$color, line width=7pt] (90+360/$camsize*\s:5) -- (90+360/$camsize*\s:5.5);
    }
  \end{tikzpicture}
\end{document}
""")


for idx, camsize in enumerate([43, 47, 51, 53, 59]):
    with open(os.path.join(OUTPUT_DIR,
                           'wheel_psi%d_%d.tex' % (idx+1, camsize)), 'w') as f:
        f.write(tmpl.substitute(camsize=camsize, color='AlexRed'))

for idx, camsize in enumerate([41, 31, 29, 26, 23]):
    with open(os.path.join(OUTPUT_DIR,
                           'wheel_chi%d_%d.tex' % (idx+1, camsize)), 'w') as f:
        f.write(tmpl.substitute(camsize=camsize, color='NavyBlue'))

for idx, camsize in enumerate([37, 61]):
    with open(os.path.join(OUTPUT_DIR,
                           'wheel_mu%d_%d.tex' % (idx+1, camsize)), 'w') as f:
        f.write(tmpl.substitute(camsize=camsize, color='OliveGreen'))
