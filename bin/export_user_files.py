import sys
import os
import shutil
import subprocess

MYSQL_CONF = '/etc/mysql/my.cnf'
MYSQL_DATA_DIR_DEFAULT = "/var/lib/mysql"
MYSQL_DATA_DIR_HOST = "/export/mysql/"

GENOME_DATA_DIR = "/export/genome_data"

def change_path( src ):
    """
        src will be copied to /export/`src` and a symlink will be placed in src pointing to /export/
    """
    if os.path.exists( src ):
        dest = os.path.join( '/export/', src.strip('/') )
        # if destination is empty move all files into /export/ and symlink back to source
        if not os.path.exists( dest ):
            dest_dir = os.path.dirname(dest)
            if not os.path.exists( dest_dir ):
                os.makedirs(dest_dir)
            shutil.move( src, dest )
            os.symlink( dest, src.rstrip('/') )
        # if destination exists (e.g. continuing a previous session), remove source and symlink
        else:
            if os.path.isdir( src ):
                shutil.rmtree( src )
            else:
                os.unlink( src )
            os.symlink( dest, src.rstrip('/') )

       # if destination exists (e.g. continuing a previous session), remove source and symlink
    else:
        if os.path.isdir( src ):
            shutil.rmtree( src )
        else:
            os.unlink( src )
        os.symlink( dest, src.rstrip('/') )


if __name__ == "__main__":

    if os.path.exists('/export/'):
        if not os.path.exists( GENOME_DATA_DIR ):
            subprocess.call('git clone https://github.com/UMMS-Biocore/dolphin-genome-data.git %s' % (GENOME_DATA_DIR), shell=True)

      #For mysql db
        if not os.path.exists( MYSQL_DATA_DIR_HOST ):
            subprocess.call('/usr/local/bin/mysqlstart', shell=True)
            dest_dir = os.path.dirname( MYSQL_DATA_DIR_HOST )
            if not os.path.exists( dest_dir ):
               os.makedirs(dest_dir)
            subprocess.call('cp -R %s/* %s' % (MYSQL_DATA_DIR_DEFAULT, MYSQL_DATA_DIR_HOST), shell=True)
            subprocess.call('chown -R mysql:mysql /export/mysql/', shell=True)

        new_data_directory = "%s" % MYSQL_DATA_DIR_HOST
        cmd = 'sed -i "s|datadir\t\t= .*|datadir\t\t= %s|g" %s' % (new_data_directory, MYSQL_CONF)
        subprocess.call(cmd, shell=True)

