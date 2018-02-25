# dockerfiles

This directory contains Dockerfiles for Docker images that I find useful.

I run a lot of programs in Docker rather than installing them directly on a machine (e.g. with brew or apt-get).

*   I can see exactly what files are being written/edited on the host
*   I can use packages/tools that are installed with package managers I don't use very often, e.g. npm or golang, and not have to worry about getting the package manager working
*   When I get a new machine, I have them available as soon as I install Docker

In my fishconfig, I've got some shell functions that call out to these images, building them first if necessary.
