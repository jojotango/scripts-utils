#!/bin/bash

# PDF compressor script using ghostscript
# Copyright (C) 2017 Joffrey

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


DEST='pdf_compressed'

if [[ $# -ge 1 ]] && [[ $1 != '--help' ]]; then
    [[ -d "$DEST" ]] || mkdir "$DEST"

    for argv in "$@"; do
        if [[ $(file "$argv" | cut -d' ' -f2) == 'PDF' ]]; then
            printf "Compress ==> %b... " "$argv" 
            gs -sDEVICE=pdfwrite \
               -dCompatibilityLevel=1.4 \
               -dPDFSETTINGS=/screen \
               -dNOPAUSE \
               -dQUIET \
               -dBATCH \
               -sOutputFile="$DEST/$argv" "$argv" && printf "Ok\n"
        fi
    done
else
    script=$(basename "$0")

    echo "$script compress PDF files in '$DEST/' current directorie"
    echo 'Usage exemple:'
    echo "    $script file1.pdf file2.pdf"
    echo "    $script *.pdf"
fi
