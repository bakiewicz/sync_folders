# Sync folders program

## Comments

- Synchronization was implemented with an infinite loop that calls the sync function at an interval defined from command line arguments

- Logging was implemented with Python's built-in library 'logging', with logs saved to a log file and printed in the console output

- The folder paths, sync interval and log file path are received from command line arguments, using built-in library argparse with optionals to define these arguments when starting the program. The optional arguments for each of them are:
    - 's' for the path to the source folder
    - 'r' for the path to the replica folder
    - 'i' for the sync interval in seconds
    - 'l' for the path to the log file

- The program can be called like this:
    ```bash
    python3 main.py -s path/to/source -r path/to/replica -i interval_in_seconds -l path/to/log_file

- The 'sync_folders' function receives source_folder and replica_folder from command line arguments, and the logger initialized in 'create_logger'. It first checks if replica folder exists and if not, creates it. It then loops through all of source folder files and directories using 'os.walk' function, calling 'add_new_source_content' helper function. It then loops the same way through replica_folder and calls 'remove_extra_content' function, but with 'topdown' argument set to false, so it starts from the deepest levels, enabling deletion of both files and directories without conflict.

- Helper functions:
    - 'create_logger' receives the path for the log file, initializes the logger for console printing and file writing

    - 'add_new_source_content' checks if received 'source_path' argument is a directory or a file, if it exists in 'target_path' and, in case it is a file, checks if it was modified either in source or replica since last sync, and copies the file or create the directory

    - 'remove_extra_content' checks if content exists in source folder. If not, it checks if it is a file or a directory and handles removal from replica


