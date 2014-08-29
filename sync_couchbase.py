#!/usr/bin/env python

# ==============================================================================
# Name          :   sync_couchbase.py
#
# Description   :   This script allows a user to sync couchbase bucket between
#                   two instances of the database.
#
# Version       :   1.0.0
#
# Author        :   Santhoshkumar Settipalli
#
# Usage         :   sync_couchbase.py
#
#                   Sync CouchBase data between two nodes.
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

# Source the default file.
import os
import sys
import fcntl
import logging
import logging.handlers
import settings

from couchbase import Couchbase

class SyncCouchBase:

    """
    Allows a user to sync couchbase data between two nodes.
    """

    # Reference to logging modules.
    logger = None
    handler = None

    logging_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }


    # === FUNCTION ===========================================================
    # Name                : log
    #
    # Description         : is used to log messages into a file (configured in
    #                       logger) - default log message level would be 'debug'.
    #
    # Return value        : none.
    #
    # Since               : v1.0
    # ========================================================================
 
    def log(self, level='debug', msg=""):
        self.logger.log(self.logging_levels.get(level), msg)


    # === FUNCTION ===========================================================
    # Name                : run_once
    #
    # Description         : is used to make sure that only one instance of the
    #                       current program in executed at any point of time.
    #
    # Return value        : none.
    #
    # Since               : v1.0
    # ========================================================================

    def run_once(self):
        global fh
        fh = open(os.path.realpath(__file__), 'r')
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
            print "Multiple instance of the program are not supported."
            os._exit(1)


    # === FUNCTION ===========================================================
    # Name                : sync_bucket
    #
    # Description         : Read data from node 1 and sync it into node 2.
    #
    # Return value        : None
    #
    # Since               : v1.0
    # ========================================================================

    def sync_bucket(self):
        try:
            from_cb = Couchbase.connect(host=settings.FROM_DB_HOST, bucket=settings.FROM_DB_BUCKET)
        except Exception as e:
            self.log(level="error", msg="Could not connect to the from db. Exception: " + str(e))
            sys.exit(1)

        try:
            to_cb = Couchbase.connect(host=settings.TO_DB_HOST, bucket=settings.TO_DB_BUCKET)
        except Exception as e:
            self.log(level="error", msg="Could not connect to the from db. Exception: " + str(e))
            sys.exit(1)

        # I have assumed that a map query named 'all' is created in the 
        # 'dev_sync' view with JavaScript code similar to the code below.
        #   function (doc, meta) {
        #       emit(meta.id, doc.type);
        #   }
        rows = from_cb.query(settings.FROM_DB_VIEW, "all", limit=100000, stale=False)
        for row in rows:
            try:          
                from_result = from_cb.get(row.key)
                self.log(level="info", msg="Found: %s in from db." % row.key)
                try:          
                    to_result  = to_cb.add(row.key, from_result.value)
                    self.log(level="info", msg="Inserted %s in to db." % row.key)
                except Exception as e:
                    to_result  = to_cb.replace(row.key, from_result.value)
                    if to_result.success == True:
                        self.log(level="info", msg="Replaced %s in to db." % row.key)
                    else:
                        self.log(level="error", msg="Failed to insert %s in to db. Error: %s" % (row.key, str(e)))
            except Exception as e:
                self.log(level="error", msg="Did not find: %s - in from db. Skipping. Error: %s" % (row.key, str(e)))

 
    # === FUNCTION ===========================================================
    # Name                : main
    #
    # Description         : Executes the core purpose of this program.
    #
    # Return value        : none.
    #
    # Since               : v1.0
    # ========================================================================

    def main(self):
        # Make sure that you are the only instance in execution.
        self.run_once()

        # Setup logging.
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger('sync_couchbase')
        self.logger.setLevel(self.logging_levels.get(settings.LOG_LEVEL))

        # Add the log message handler to the logger (1 MB per file and upto 10
        # files)
        self.handler = logging.handlers.RotatingFileHandler(
            settings.LOG_FILE, maxBytes=1048576, backupCount=10)
        self.handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(self.handler)

        # Avoid console logging - by blocking automatic propagation to the upper
        # logger module i.e. console logger.
        # self.logger.propagate = False

        self.log(level="info",  
                 msg="=============================================")
        self.log(level="info", msg="Logger initialized.")

        self.sync_bucket()

        self.log(level="info", msg="All done!")
        self.log(level="info",
                 msg="=============================================")


if __name__ == "__main__":
    sync_db = SyncCouchBase()
    sync_db.main()
