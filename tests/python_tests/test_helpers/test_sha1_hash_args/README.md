The idea is to test our target list file generator, which uses Python's hashlib module, against another SHA1 implementation.
On UNIX/Linux systems, this is "sha1sum".
On Windows, using PowerShell, it is System.Security.Cryptography.SHA1

There is a LOT that needs to be said here.
Firstly, because of how even slight changes to the input can
change the the SHA1 hash value, we need to set some ground
rules on what is to be hashed and the format it needs to be in.

1. All input files MUST be in UTF-8 with no Byte Order Mark (BOM)
   How you ensure this is platform dependent, but if you are using 
   UTF-8 as your system encoding on Linux, it should be the default.
   On Windows and macOS, you may need to run a conversion tool.

2. All output files must also be in UTF-8 with no BOM.

4. During testing, the list of targets must be converted to lowercase in the testing
   scripts and sample file generation scripts.

5. During testing, the list of targets must be sorted lexicographically after converting
   all targets to lowercase.

6. All whitespace must be stripped from each target name prior to running it through
   the hasher.  Do NOT edit the target name in place. Make a copy. Whitespace and newlines
   will be needed later when writing the file.

  
