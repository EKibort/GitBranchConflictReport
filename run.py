import git_branch_conflicts
import logging

logger = logging.getLogger('git_merge_conflicts')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

ignore_patterns = ['.*CHANGELOG','.*pubspec.yaml']
repository_path = "/repository"

logging.info("Starting for '{0}'".format(repository_path))

detector = git_branch_conflicts.ConflictDetector(repository_path, ignore_patterns)
detector.pullAllBrachesLocaly()
conflicts = detector.get_merge_conflicts()

logging.info("Finished")

