cmake_minimum_required (VERSION 2.6) 
project (ZTOP)

set (ZTOP_VERSION_MAJOR 0)
set (ZTOP_VERSION_MINOR 1)

SET(CURSES_USE_NCURSES TRUE)
SET(CURSES_NEED_NCURSES TRUE)
FIND_PACKAGE(Curses)

add_executable(ztop ztop.c RichString.c Process.c UsersTable.c Vector.c Hashtable.c RichString.c) 

target_link_libraries (ztop ncurses)