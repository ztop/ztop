ztop
====

linux data aggregator (written in Go)

Setup
===========

Since you can find several sites online that will help you setup a Go workspace, 
I will only cover the basics here.

First you will create a folder structure like this

    ztop
    |
    ----bin
    |
    ----pkg
    |
    ----src
        | 
        ----github.com
            |
            ----ztop

Then you will cd into src/github.com/ztop and use 

`git clone https(or ssh)://github.com/ztop/ztop.git`

Now while in the top level ztop directory (cd to it if you aren't there) 
set this as the go path by typing 

``export GOPATH=`pwd` ``

and now you should be able to just run

`go build ...ztop`

and it should produce an executable in the top level ztop directory. When you are 
ready to commit changes, just cd to the src/github.com/ztop/ztop directory and work 
with git straight from there.
