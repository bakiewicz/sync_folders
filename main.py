import argparse, os, logging, time, shutil


def create_logger(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger


def add_new_source_content(source_path, target_path, logger):
    if os.path.isdir(source_path):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            logger.info(f"Created directory {target_path}")
    else:
        if not os.path.exists(target_path) or os.path.getmtime(source_path) != os.path.getmtime(target_path):
            shutil.copy2(source_path, target_path)
            logger.info(f"Copied {source_path} to {target_path}")


def remove_extra_content(replica_path, source_path, logger):
    if not os.path.exists(source_path):
        if os.path.isfile(replica_path):
            os.remove(replica_path)
            logger.info(f"Removed {replica_path}")
        elif not os.listdir(replica_path):
            os.rmdir(replica_path)
            logger.info(f"Removed directory {replica_path}")


def sync_folders(source_folder, replica_folder, logger):
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    for root, dirs, files in os.walk(source_folder):
        for name in dirs + files:
            full_source_path = os.path.join(root, name)
            full_replica_path = os.path.join(root.replace(source_folder, replica_folder, 1), name)
            add_new_source_content(full_source_path, full_replica_path, logger)

    for root, dirs, files in os.walk(replica_folder, topdown=False):
        for name in files + dirs:
            remove_extra_content(os.path.join(root, name),
                                         os.path.join(root.replace(replica_folder, source_folder, 1), name),
                                         logger)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Sync Folders program')
    parser.add_argument("-s", "--source", help="Path to source folder", required=True)
    parser.add_argument("-r", "--replica", help="Path to replica folder", required=True)
    parser.add_argument("-i", "--interval", type=int, help="Interval in seconds", required=True)
    parser.add_argument("-l", "--log_file", help="Path to log file", required=True)
    args = parser.parse_args()

    logger = create_logger(args.log_file)

    while True:
        try:
            sync_folders(args.source, args.replica, logger)
            time.sleep(args.interval)
        except Exception as e:
            logger.error(f"Error: {e}")
            break

    

