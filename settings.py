#!/usr/bin/env python

# ==============================================================================
# Name          :   settings.py
#
# Description   :   This script contains the configuration information for the
#                   sync_couchbase program.
#
# Version       :   1.0.0
#
# Author        :   Santhoshkumar Settipalli
#
# Usage         :   Import this script.
#
# Change log    :
#   29-Aug-2014 :    Santhoshkumar Settipalli (Santhoshkumar.Settipalli@polycom.com)
#                    Initial version.
#
# Copyright (c) Santhoshkumar Settipalli 2014. All rights are goverened by the
# below License Agreement.
# 
# The MIT License (MIT)
#
# Copyright (c) 2014 Santhoshkumar Settipalli
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

import os

# Location of the log file to log user actions.
LOG_FOLDER = "log"
LOG_FILE = LOG_FOLDER + "/sync_couchbase.log"
# Supported value: 'debug', 'info', 'warning', 'error', 'critical'
LOG_LEVEL = "debug"

# Update the values below.
FROM_DB_HOST = "127.0.0.2"  # IP address of the CouchBase Host (From)
FROM_DB_ADMIN = "admin"
FROM_DB_BUCKET = "frombucket"
FROM_DB_VIEW = "dev_sync"

# Use the below sample map query for the dev_sync view (in JavaScript)
# 
# function (doc, meta) {
#   emit(meta.id, doc.type);
# }

# Update the values below.
TO_DB_HOST = "127.0.0.1"    # IP address of the CouchBase Host (To)
TO_DB_ADMIN = "Administrator"
TO_DB_BUCKET = "tobucket"
# No view for TO_DB because a view is used to fetch keys and use those to
# read data from from_db and insert data in to_db.
