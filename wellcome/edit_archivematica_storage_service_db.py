#!/usr/bin/env python
"""
I had a bug in the Archivematica storage service where it was recording the
wrong storage space for packages in the Wellcome Storage Service, so downloads
were broken.

This is a script I wrote to correct the error, which runs inside the
storage-service container.

I don't expect to use this exact script again, but I'm saving it as a possible
base for the next time I need to edit the Archivematica databases.

"""

import termcolor

import django
django.setup()

from locations.models.package import Package

for pkg in Package.objects.all():
#    print(pkg.misc_attributes)

    print(
        "External identifier is %s, space is %s" %
        (termcolor.colored(pkg.misc_attributes["wellcome.external_identifier"], "red"),
        termcolor.colored(pkg.misc_attributes["wellcome.space"], "red"))
    )

    if (
        pkg.misc_attributes["wellcome.external_identifier"].isnumeric() and
        pkg.misc_attributes["wellcome.space"] == "born-digital"
    ):
        pkg.misc_attributes["wellcome.space"] = "born-digital-accessions"
        pkg.save()

       # break