# Sakura FreeBSD Fix Log

Start: 2026-01-31T06:43:33.7119825+09:00

Requirement already satisfied: pip in /home/garyo/local/python/lib/python3.6/site-packages (21.0.1)
Collecting pip
  Using cached pip-25.0.1-py3-none-any.whl (1.8 MB)
Requirement already satisfied: setuptools in /home/garyo/local/python/lib/python3.6/site-packages (40.6.2)
Collecting setuptools
  Using cached setuptools-75.3.3-py3-none-any.whl (1.3 MB)
Collecting wheel
  Using cached wheel-0.45.1-py3-none-any.whl (72 kB)
Installing collected packages: wheel, setuptools, pip
  Attempting uninstall: setuptools
    Found existing installation: setuptools 40.6.2
    Not uninstalling setuptools at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'setuptools'. No files were found to uninstall.
  Attempting uninstall: pip
    Found existing installation: pip 21.0.1
    Not uninstalling pip at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'pip'. No files were found to uninstall.
Successfully installed pip-25.0.1 setuptools-75.3.3 wheel-0.45.1
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Collecting fastapi==0.104.1
  Using cached fastapi-0.104.1-py3-none-any.whl (92 kB)
Collecting uvicorn==0.24.0
  Using cached uvicorn-0.24.0-py3-none-any.whl (59 kB)
Collecting pydantic==2.5.0
  Using cached pydantic-2.5.0-py3-none-any.whl (407 kB)
ERROR: Could not find a version that satisfies the requirement pydantic-core==2.14.0
ERROR: No matching distribution found for pydantic-core==2.14.0
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Unmatched '''.
Version: ImageMagick 6.9.12-34 Q16 amd64 2021-12-22 https://imagemagick.org
Copyright: (C) 1999-2021 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher Modules 
Delegates (built-in): bzlib fontconfig freetype jbig jng jp2 jpeg ltdl lzma png tiff webp xml zlib
Usage: garyo [options ...] [ file ]

Image Settings:
  -adjoin              join images into a single multi-image file
  -border              include window border in the output image
  -channel type        apply option to select image channels
  -colorspace type     alternate image colorspace
  -comment string      annotate image with comment
  -compress type       type of pixel compression when writing the image
  -define format:option
                       define one or more image format options
  -density geometry    horizontal and vertical density of the image
  -depth value         image depth
  -descend             obtain image by descending window hierarchy
  -display server      X server to contact
  -dispose method      layer disposal method
  -dither method       apply error diffusion to image
  -delay value         display the next image after pausing
  -encipher filename   convert plain pixels to cipher pixels
  -endian type         endianness (MSB or LSB) of the image
  -encoding type       text encoding type
  -filter type         use this filter when resizing an image
  -format "string"     output formatted image characteristics
  -frame               include window manager frame
  -gravity direction   which direction to gravitate towards
  -identify            identify the format and characteristics of the image
  -interlace type      None, Line, Plane, or Partition
  -interpolate method  pixel color interpolation method
  -label string        assign a label to an image
  -limit type value    Area, Disk, Map, or Memory resource limit
  -monitor             monitor progress
  -page geometry       size and location of an image canvas
  -pause seconds       seconds delay between snapshots
  -pointsize value     font point size
  -quality value       JPEG/MIFF/PNG compression level
  -quiet               suppress all warning messages
  -regard-warnings     pay attention to warning messages
  -repage geometry     size and location of an image canvas
  -respect-parentheses settings remain in effect until parenthesis boundary
  -sampling-factor geometry
                       horizontal and vertical sampling factor
  -scene value         image scene number
  -screen              select image from root window
  -seed value          seed a new sequence of pseudo-random numbers
  -set property value  set an image property
  -silent              operate silently, i.e. don't ring any bells 
  -snaps value         number of screen snapshots
  -support factor      resize support: > 1.0 is blurry, < 1.0 is sharp
  -synchronize         synchronize image to storage device
  -taint               declare the image as modified
  -transparent-color color
                       transparent color
  -treedepth value     color tree depth
  -verbose             print detailed information about the image
  -virtual-pixel method
                       Constant, Edge, Mirror, or Tile
  -window id           select window with this id or name

Image Operators:
  -annotate geometry text
                       annotate the image with text
  -colors value        preferred number of colors in the image
  -crop geometry       preferred size and location of the cropped image
  -encipher filename   convert plain pixels to cipher pixels
  -geometry geometry   preferred size or location of the image
  -help                print program options
  -monochrome          transform image to black and white
  -negate              replace every pixel with its complementary color 
  -quantize colorspace reduce colors in this colorspace
  -resize geometry     resize the image
  -rotate degrees      apply Paeth rotation to the image
  -strip               strip image of all profiles and comments
  -thumbnail geometry  create a thumbnail of the image
garyo: delegate library support not built-in `' (X11) @ error/import.c/ImportImageCommand/1286.
  -transparent color   make this color transparent within the image
  -trim                trim image edges
  -type type           image type

Miscellaneous Options:
  -debug events        display copious debugging information
  -help                print program options
  -list type           print a list of supported option arguments
  -log format          format of debugging information
  -version             print version information

By default, 'file' is written in the MIFF image format.  To
specify a particular image format, precede the filename with an image
format name and a colon (i.e. ps:image) or specify the image type as
the filename suffix (i.e. image.ps).  Specify 'file' as '-' for
standard input or output.
Version: ImageMagick 6.9.12-34 Q16 amd64 2021-12-22 https://imagemagick.org
Copyright: (C) 1999-2021 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher Modules 
Delegates (built-in): bzlib fontconfig freetype jbig jng jp2 jpeg ltdl lzma png tiff webp xml zlib
Usage: garyo [options ...] [ file ]

Image Settings:
  -adjoin              join images into a single multi-image file
  -border              include window border in the output image
garyo: delegate library support not built-in `' (X11) @ error/import.c/ImportImageCommand/1286.
  -channel type        apply option to select image channels
  -colorspace type     alternate image colorspace
  -comment string      annotate image with comment
  -compress type       type of pixel compression when writing the image
  -define format:option
                       define one or more image format options
  -density geometry    horizontal and vertical density of the image
  -depth value         image depth
  -descend             obtain image by descending window hierarchy
  -display server      X server to contact
  -dispose method      layer disposal method
  -dither method       apply error diffusion to image
  -delay value         display the next image after pausing
  -encipher filename   convert plain pixels to cipher pixels
  -endian type         endianness (MSB or LSB) of the image
  -encoding type       text encoding type
  -filter type         use this filter when resizing an image
  -format "string"     output formatted image characteristics
  -frame               include window manager frame
  -gravity direction   which direction to gravitate towards
  -identify            identify the format and characteristics of the image
  -interlace type      None, Line, Plane, or Partition
  -interpolate method  pixel color interpolation method
  -label string        assign a label to an image
  -limit type value    Area, Disk, Map, or Memory resource limit
  -monitor             monitor progress
  -page geometry       size and location of an image canvas
  -pause seconds       seconds delay between snapshots
  -pointsize value     font point size
  -quality value       JPEG/MIFF/PNG compression level
  -quiet               suppress all warning messages
  -regard-warnings     pay attention to warning messages
  -repage geometry     size and location of an image canvas
  -respect-parentheses settings remain in effect until parenthesis boundary
  -sampling-factor geometry
                       horizontal and vertical sampling factor
  -scene value         image scene number
  -screen              select image from root window
  -seed value          seed a new sequence of pseudo-random numbers
  -set property value  set an image property
  -silent              operate silently, i.e. don't ring any bells 
  -snaps value         number of screen snapshots
  -support factor      resize support: > 1.0 is blurry, < 1.0 is sharp
  -synchronize         synchronize image to storage device
  -taint               declare the image as modified
  -transparent-color color
                       transparent color
  -treedepth value     color tree depth
  -verbose             print detailed information about the image
  -virtual-pixel method
                       Constant, Edge, Mirror, or Tile
  -window id           select window with this id or name

Image Operators:
  -annotate geometry text
                       annotate the image with text
  -colors value        preferred number of colors in the image
  -crop geometry       preferred size and location of the cropped image
  -encipher filename   convert plain pixels to cipher pixels
  -geometry geometry   preferred size or location of the image
  -help                print program options
  -monochrome          transform image to black and white
  -negate              replace every pixel with its complementary color 
  -quantize colorspace reduce colors in this colorspace
  -resize geometry     resize the image
  -rotate degrees      apply Paeth rotation to the image
  -strip               strip image of all profiles and comments
  -thumbnail geometry  create a thumbnail of the image
  -transparent color   make this color transparent within the image
  -trim                trim image edges
  -type type           image type

Miscellaneous Options:
  -debug events        display copious debugging information
  -help                print program options
  -list type           print a list of supported option arguments
  -log format          format of debugging information
  -version             print version information

By default, 'file' is written in the MIFF image format.  To
specify a particular image format, precede the filename with an image
format name and a colon (i.e. ps:image) or specify the image type as
the filename suffix (i.e. image.ps).  Specify 'file' as '-' for
standard input or output.
Version: ImageMagick 6.9.12-34 Q16 amd64 2021-12-22 https://imagemagick.org
Copyright: (C) 1999-2021 ImageMagick Studio LLC
License: https://imagemagick.org/script/license.php
Features: Cipher Modules 
Delegates (built-in): bzlib fontconfig freetype jbig jng jp2 jpeg ltdl lzma png tiff webp xml zlib
Usage: garyo [options ...] [ file ]

Image Settings:
  -adjoin              join images into a single multi-image file
  -border              include window border in the output image
  -channel type        apply option to select image channels
  -colorspace type     alternate image colorspace
  -comment string      annotate image with comment
  -compress type       type of pixel compression when writing the image
  -define format:option
                       define one or more image format options
  -density geometry    horizontal and vertical density of the image
  -depth value         image depth
  -descend             obtain image by descending window hierarchy
  -display server      X server to contact
  -dispose method      layer disposal method
  -dither method       apply error diffusion to image
  -delay value         display the next image after pausing
  -encipher filename   convert plain pixels to cipher pixels
  -endian type         endianness (MSB or LSB) of the image
  -encoding type       text encoding type
  -filter type         use this filter when resizing an image
  -format "string"     output formatted image characteristics
  -frame               include window manager frame
  -gravity direction   which direction to gravitate towards
  -identify            identify the format and characteristics of the image
  -interlace type      None, Line, Plane, or Partition
  -interpolate method  pixel color interpolation method
  -label string        assign a label to an image
  -limit type value    Area, Disk, Map, or Memory resource limit
  -monitor             monitor progress
  -page geometry       size and location of an image canvas
  -pause seconds       seconds delay between snapshots
  -pointsize value     font point size
  -quality value       JPEG/MIFF/PNG compression level
  -quiet               suppress all warning messages
  -regard-warnings     pay attention to warning messages
  -repage geometry     size and location of an image canvas
  -respect-parentheses settings remain in effect until parenthesis boundary
  -sampling-factor geometry
                       horizontal and vertical sampling factor
  -scene value         image scene number
  -screen              select image from root window
  -seed value          seed a new sequence of pseudo-random numbers
  -set property value  set an image property
  -silent              operate silently, i.e. don't ring any bells 
  -snaps value         number of screen snapshots
  -support factor      resize support: > 1.0 is blurry, < 1.0 is sharp
  -synchronize         synchronize image to storage device
  -taint               declare the image as modified
  -transparent-color color
                       transparent color
  -treedepth value     color tree depth
  -verbose             print detailed information about the image
  -virtual-pixel method
                       Constant, Edge, Mirror, or Tile
  -window id           select window with this id or name

Image Operators:
  -annotate geometry text
                       annotate the image with text
  -colors value        preferred number of colors in the image
  -crop geometry       preferred size and location of the cropped image
  -encipher filename   convert plain pixels to cipher pixels
  -geometry geometry   preferred size or location of the image
  -help                print program options
  -monochrome          transform image to black and white
  -negate              replace every pixel with its complementary color 
  -quantize colorspace reduce colors in this colorspace
  -resize geometry     resize the image
  -rotate degrees      apply Paeth rotation to the image
  -strip               strip image of all profiles and comments
  -thumbnail geometry  create a thumbnail of the image
garyo: delegate library support not built-in `' (X11) @ error/import.c/ImportImageCommand/1286.
  -transparent color   make this color transparent within the image
  -trim                trim image edges
  -type type           image type

Miscellaneous Options:
  -debug events        display copious debugging information
  -help                print program options
  -list type           print a list of supported option arguments
  -log format          format of debugging information
  -version             print version information

By default, 'file' is written in the MIFF image format.  To
specify a particular image format, precede the filename with an image
format name and a colon (i.e. ps:image) or specify the image type as
the filename suffix (i.e. image.ps).  Specify 'file' as '-' for
standard input or output.
Badly placed ()'s.
Unmatched '''.
/home/garyo/magic-box-ai/venv/bin/python3: Error while finding module specification for 'scripts.init_db' (ModuleNotFoundError: No module named 'scripts')
ls: magicboxai.db: No such file or directory
/home/garyo/magic-box-ai/venv/bin/python3: No module named pytest
/home/garyo/magic-box-ai/venv/bin/python3: No module named pytest
Requirement already satisfied: gunicorn in ./venv/lib/python3.8/site-packages (23.0.0)
Requirement already satisfied: packaging in ./venv/lib/python3.8/site-packages (from gunicorn) (26.0)
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
System.Management.Automation.RemoteException
Error: class uri 'uvicorn.workers.UvicornWorker' invalid or not found: 
System.Management.Automation.RemoteException
[Traceback (most recent call last):
  File "/home/garyo/magic-box-ai/venv/lib/python3.8/site-packages/gunicorn/util.py", line 110, in load_class
    mod = importlib.import_module('.'.join(components))
  File "/usr/local/lib/python3.8/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
  File "<frozen importlib._bootstrap>", line 991, in _find_and_load
  File "<frozen importlib._bootstrap>", line 961, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
  File "<frozen importlib._bootstrap>", line 991, in _find_and_load
  File "<frozen importlib._bootstrap>", line 973, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'uvicorn'
]
System.Management.Automation.RemoteException
Unmatched '''.
\342\234\205: Command not found.
Illegal variable name.
Illegal variable name.
1.: Command not found.
2.: Command not found.
3.: Command not found.
4.: Command not found.
5.: Command not found.
-: Command not found.
-: Command not found.
EOF: Command not found.
Unmatched '''.

End: 2026-01-31T06:44:41.7491286+09:00

/home/garyo/magic-box-ai/venv/bin/pip
pip 21.0.1 from /home/garyo/local/python/lib/python3.6/site-packages/pip (python 3.8)
/home/garyo/magic-box-ai/venv/bin/python
Python 3.8.12

--- RERUN 2026-01-31T06:45:40.3437466+09:00 ---

Requirement already satisfied: pip in /home/garyo/local/python/lib/python3.6/site-packages (21.0.1)
Collecting pip
  Using cached pip-25.0.1-py3-none-any.whl (1.8 MB)
Requirement already satisfied: setuptools in /home/garyo/local/python/lib/python3.6/site-packages (40.6.2)
Collecting setuptools
  Using cached setuptools-75.3.3-py3-none-any.whl (1.3 MB)
Requirement already satisfied: wheel in ./venv/lib/python3.8/site-packages (0.45.1)
Installing collected packages: setuptools, pip
  Attempting uninstall: setuptools
    Found existing installation: setuptools 40.6.2
    Not uninstalling setuptools at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'setuptools'. No files were found to uninstall.
  Attempting uninstall: pip
    Found existing installation: pip 21.0.1
    Not uninstalling pip at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'pip'. No files were found to uninstall.
Successfully installed pip-25.0.1 setuptools-75.3.3
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Collecting fastapi==0.104.1
  Using cached fastapi-0.104.1-py3-none-any.whl (92 kB)
Collecting uvicorn==0.24.0
  Using cached uvicorn-0.24.0-py3-none-any.whl (59 kB)
Collecting pydantic==2.5.0
  Using cached pydantic-2.5.0-py3-none-any.whl (407 kB)
ERROR: Could not find a version that satisfies the requirement pydantic-core==2.14.0
ERROR: No matching distribution found for pydantic-core==2.14.0
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
imports): -c: line 1: syntax error near unexpected token `OK:'
imports): -c: line 1: ` cd ~/magic-box-ai; source venv/bin/activate; /home/garyo/magic-box-ai/venv/bin/python -m pip list | grep -E fastapi|uvicorn|pydantic; /home/garyo/magic-box-ai/venv/bin/python -c import fastapi, uvicorn, pydantic; print(OK:'
/home/garyo/magic-box-ai/venv/bin/python: Error while finding module specification for 'scripts.init_db' (ModuleNotFoundError: No module named 'scripts')
ls: magicboxai.db: No such file or directory
/home/garyo/magic-box-ai/venv/bin/python: No module named pytest
/home/garyo/magic-box-ai/venv/bin/python: No module named pytest
Requirement already satisfied: gunicorn in ./venv/lib/python3.8/site-packages (23.0.0)
Requirement already satisfied: packaging in ./venv/lib/python3.8/site-packages (from gunicorn) (26.0)
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
System.Management.Automation.RemoteException
Error: class uri 'uvicorn.workers.UvicornWorker' invalid or not found: 
System.Management.Automation.RemoteException
[Traceback (most recent call last):
  File "/home/garyo/magic-box-ai/venv/lib/python3.8/site-packages/gunicorn/util.py", line 110, in load_class
    mod = importlib.import_module('.'.join(components))
  File "/usr/local/lib/python3.8/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
  File "<frozen importlib._bootstrap>", line 991, in _find_and_load
  File "<frozen importlib._bootstrap>", line 961, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
  File "<frozen importlib._bootstrap>", line 991, in _find_and_load
  File "<frozen importlib._bootstrap>", line 973, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'uvicorn'
]
System.Management.Automation.RemoteException
Illegal variable name.
bash: -c: line 1: syntax error near unexpected token `'OK: imports''
bash: -c: line 1: ` cd ~/magic-box-ai; source venv/bin/activate; /home/garyo/magic-box-ai/venv/bin/python -m pip list | egrep fastapi|uvicorn|pydantic; /home/garyo/magic-box-ai/venv/bin/python -c import fastapi, uvicorn, pydantic; print('OK: imports')'
Illegal variable name.
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'fastapi'
cat: SETUP_FIX_COMPLETE.txt
: No such file or directory
cat: SETUP_FIX_COMPLETE.txt
: No such file or directory
/home/garyo
ls: /home/garyo/magic-box-ai
: No such file or directory
ls: /home/garyo
: No such file or directory
HOME=/home/garyo
/home/garyo
total 4708
drwx------   34 garyo  users     1536 Jan 31 06:29 .
drwxr-xr-x  136 root   wheel     3072 Jan 26 17:26 ..
drwx------    3 garyo  users      512 Feb 10  2021 .cache
-rw-r--r--    1 garyo  users     1413 Feb 10  2021 .cshrc
-rw-r--r--    1 garyo  users      116 Oct 11 08:06 .fd_history
drwxr-xr-x    4 garyo  users      512 Apr  7  2011 .gem
-rw-------    1 garyo  users     3226 Jan 31 06:29 .history
-rw-------    1 garyo  users       73 Apr  7  2011 .lesshst
drwx------    4 garyo  users      512 Jan 17  2025 .local
-rw-r--r--    1 garyo  users      255 Jul 14  2004 .login
-rw-r--r--    1 garyo  users      165 Jul 14  2004 .login_conf
-rw-------    1 garyo  users      371 Jul 14  2004 .mail_aliases
-rw-r--r--    1 garyo  users      331 Jul 14  2004 .mailrc
-rw-r--r--    1 garyo  users        3 Jan 17  2025 .my.version
-rw----r--    1 garyo  users        4 Nov  6  2013 .perl.version
drwxr-xr-x    2 garyo  users      512 Jan 17  2025 .php.config
-rw-r--r--    1 garyo  users        0 Jan 17  2025 .php.module
-rw-r--r--    1 garyo  users        4 Jan 17  2025 .php.version
-rw-r--r--    1 garyo  users      801 Jul 14  2004 .profile
-rw-------    1 garyo  users       28 Aug 28 20:53 .python_history
-rw-------    1 garyo  users      276 Jul 14  2004 .rhosts
drwxr-xr-x    3 garyo  users      512 Aug 29  2024 .rs-vendor
-rw----r--    1 garyo  users        4 Mar 20  2023 .ruby.version
-rw-r--r--    1 garyo  users      852 Jul 14  2004 .shrc
drwx------    2 garyo  users      512 Jan 31 05:14 .spamassassin
-rw-------    1 garyo  users        3 May 15  2007 .sqlite_history
drwx------    2 garyo  users      512 Jan 31 06:15 .ssh
drwxr-xr-x    3 garyo  users      512 May  7  2007 .subversion
-rw-r--r--    1 garyo  users        0 Jan 27 16:51 1
drwx------   20 garyo  users      512 Jan 30  2025 MailBox
drwxr-xr-x    3 garyo  users      512 Sep 13  2007 RSA
drwxr-xr-x    2 garyo  users      512 Feb  6  2007 backup
drwxr-xr-x    2 garyo  users      512 May  7  2007 bin
-rwxr-xr-x    1 garyo  users     6451 Aug 29 14:25 booktracker_auth.py
-rw-r--r--    1 garyo  users   215357 Jan 31 00:00 cron.log
-rw-r--r--    1 garyo  users  4296662 Jan 31 06:00 cronxperiabot.log
drwxr-xr-x    3 garyo  users      512 Jan 27 14:54 data
drwxr-xr-x    3 garyo  users      512 Aug 28  2013 db
-rw-------    1 garyo  users      376 Jan 27 16:44 dead.letter
-rwxr-xr-x    1 garyo  users      933 Aug 29 14:38 deploy_booktracker.sh
drwxr-xr-x   14 garyo  users     2560 Jun  4  2014 fml
drwxr-xr-x    2 garyo  users      512 May  7  2007 include
drwxr-xr-x    4 garyo  users      512 May  7  2007 lib
drwxr-xr-x   10 garyo  users      512 Feb 10  2021 local
drwxr-xr-x    3 garyo  users    23552 Jan 31 00:05 log
drwxr-xr-x    5 garyo  users      512 Aug 29 18:52 logs
drwxr-xr-x    7 garyo  users     1024 Jan 31 06:48 magic-box-ai
drwx------   12 garyo  users      512 Jan 17  2025 ports
drwxr-xrwx   15 garyo  users      512 Feb 12  2025 project
drwxr-xr-x    2 garyo  users      512 Jan 27  2015 sakura_pocket
drwxr-xr-x    2 garyo  users      512 Feb  3  2007 sblo_files
drwx---r-x    2 garyo  users      512 Aug 29 14:25 secrets
drwxr-xr-x    6 garyo  users      512 Aug  8  2018 soft
drwxr-xr-x    7 garyo  users      512 May  7  2007 svn-repos
drwxr-xr-x    2 garyo  users      512 Apr  8  2011 temp
drwx------    4 garyo  users      512 Dec 21 01:52 var
drwxr-xr-x    3 garyo  users      512 Feb 10  2021 workspace
drwx---r-x   38 garyo  users     1024 Jan 27 08:19 www
ls: ~
: No such file or directory

--- RERUN2 2026-01-31T06:50:05.2898093+09:00 (cd magic-box-ai) ---

Requirement already satisfied: pip in /home/garyo/local/python/lib/python3.6/site-packages (21.0.1)
Collecting pip
  Using cached pip-25.0.1-py3-none-any.whl (1.8 MB)
Requirement already satisfied: setuptools in /home/garyo/local/python/lib/python3.6/site-packages (40.6.2)
Collecting setuptools
  Using cached setuptools-75.3.3-py3-none-any.whl (1.3 MB)
Requirement already satisfied: wheel in ./venv/lib/python3.8/site-packages (0.45.1)
Installing collected packages: setuptools, pip
  Attempting uninstall: setuptools
    Found existing installation: setuptools 40.6.2
    Not uninstalling setuptools at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'setuptools'. No files were found to uninstall.
  Attempting uninstall: pip
    Found existing installation: pip 21.0.1
    Not uninstalling pip at /home/garyo/local/python/lib/python3.6/site-packages, outside environment /home/garyo/magic-box-ai/venv
    Can't uninstall 'pip'. No files were found to uninstall.
Successfully installed pip-25.0.1 setuptools-75.3.3
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Collecting fastapi==0.104.1
  Using cached fastapi-0.104.1-py3-none-any.whl (92 kB)
Collecting uvicorn==0.24.0
  Using cached uvicorn-0.24.0-py3-none-any.whl (59 kB)
Collecting pydantic==2.5.0
  Using cached pydantic-2.5.0-py3-none-any.whl (407 kB)
ERROR: Could not find a version that satisfies the requirement pydantic-core==2.14.0
ERROR: No matching distribution found for pydantic-core==2.14.0
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'fastapi'
/home/garyo/magic-box-ai/venv/bin/python: Error while finding module specification for 'scripts.init_db' (ModuleNotFoundError: No module named 'scripts')
ls: magicboxai.db
: No such file or directory
/home/garyo/magic-box-ai/venv/bin/python: No module named pytest
tail: test_results_fixed.txt
: No such file or directory
Requirement already satisfied: gunicorn in ./venv/lib/python3.8/site-packages (23.0.0)
Requirement already satisfied: packaging in ./venv/lib/python3.8/site-packages (from gunicorn) (26.0)
WARNING: You are using pip version 21.0.1; however, version 25.0.1 is available.
You should consider upgrading via the '/home/garyo/magic-box-ai/venv/bin/python -m pip install --upgrade pip' command.
timeout: exec(gunicorn): No such file or directory
bash: line 3: $'true\r': command not found
cat: SETUP_FIX_COMPLETE.txt
: No such file or directory
Illegal variable name.
SHELL=
SH0=
/usr/local/bin/bash
bashok
cat: SETUP_FIX_COMPLETE.txt
: No such file or directory
HOME=/home/garyo
bash: line 2: $'pwd\r': command not found
test
bash: -c: line 1: syntax error near unexpected token `('
bash: -c: line 1: `cd /home/garyo/magic-box-ai; { echo ⚠️ MagicBoxAI Sakura FreeBSD Setup - Fixed (PARTIAL); echo "; echo Date: $(date); echo Host: $(hostname); echo "; echo 結果:; echo - pydantic-core wheel が見つからず依存関係インストール失敗; echo - pytest/uvicorn 未導入のためテスト/起動が未完了; echo "; echo 次の作業:; echo - pydantic-core の利用可能な wheel 版を確認（Python/OS対応）; echo - 代替バージョンで再試行 or Python/OS更新; } > SETUP_FIX_COMPLETE.txt; cat SETUP_FIX_COMPLETE.txt'
bash: -c: line 1: syntax error near unexpected token `('
bash: -c: line 1: `cd /home/garyo/magic-box-ai; { echo MagicBoxAI Sakura FreeBSD Setup - Fixed (PARTIAL); echo "; echo Date: $(date); echo Host: $(hostname); echo "; echo Result:; echo - pydantic-core wheel not found; dependency install failed; echo - pytest/uvicorn not installed; echo "; echo Next:; echo - Find compatible pydantic-core wheel for FreeBSD/Python 3.8; echo - Retry install or upgrade Python/OS; } > SETUP_FIX_COMPLETE.txt; cat SETUP_FIX_COMPLETE.txt'
bash: line 1: base64: command not found
Sat Jan 31 06:54:58 JST 2026
www1026.sakura.ne.jp
