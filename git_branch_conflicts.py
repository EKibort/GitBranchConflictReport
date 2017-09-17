import logging
import sys
import re
from git import Repo
from git.exc import GitCommandError

#class Conflict(dict):
class Conflict:
    def __init__(self, branch1_name, branch2_name, conflicted_paths):
        self.branch1_name = branch1_name
        self.branch2_name = branch2_name
        self.conflicted_paths = conflicted_paths
        #dict.__init__(self, branch1_name=branch1_name, branch2_name=branch2_name, conflicted_paths = conflicted_paths)

    def __str__(self):
        return "'{0}' - '{1}' : '{2}'".format(self.branch1_name, self.branch2_name, str(self.conflicted_paths))

    def __repr__(self):
        return self. __str__()

class ConflictDetector:        
    def __init__(self, repository_path, ignore_patterns=[]):
        self._repo = Repo(repository_path)        
        self._ignore_patterns = []
        for p in ignore_patterns:
            self._ignore_patterns.append(re.compile(p))
           

    def _reset(self):
        self._repo.git.reset('--hard', 'HEAD')
        self._repo.git.clean('-xdf')

    def _isIgnoredFile(self, filename):
        for p in self._ignore_patterns:
            if p.match(filename):
                return True
        return False

    def _getConflictedFiles(self, branch1, branch2):
        conflicts = [];
        unmerged_blobs = self._repo.index.unmerged_blobs()
        logging.info("\t\tDetect conflicts in files:")
        for path in unmerged_blobs:            
            if not self._isIgnoredFile(path):
                logging.info("\t\t\t'{0}'".format(path))                    
                conflicts.append(path)
                #print(dir(unmerged_blobs[path][0]))
            else:
                logging.info("\t\t\t'{0}' - ignored".format(path))

        return conflicts

    def pullAllBrachesLocaly(self):
        #   self._repo.git.remote.prune("origin")
        logging.info("Fetching branches ....")
        self._repo.git.fetch('--all')
        for r in self._repo.remotes:
            for b1 in r.refs:
                tracking = ""
                try:
                        self._repo.git.checkout(b1, "-t")
                        tracking = " - fetched"
                except GitCommandError as e:
                        if e.status != 128:
                                raise
                        else:
                                tracking = " - already tracked"
                logging.info("\t'{0}'{1}".format(b1.name, tracking))
                        
        return None


    def get_merge_conflicts(self):
        conflicts={}

        for b1 in self._repo.branches:
            logging.info("Checkout '{0}'".format(b1.name))
            self._reset()
            self._repo.git.checkout(b1)
            
            for b2 in reversed(self._repo.branches):
                    if b1==b2:
                            break
                    try:
                            logging.info("\tMerging with '{0}'".format(b2.name))
                            self._reset()
                            res = self._repo.git.merge(b2)
                    except GitCommandError as e:
                            if e.status == 1:
                                conflicted_files = self._getConflictedFiles(b1, b2)
                                if conflicted_files:
                                    conflicts.setdefault(b1.name, []).append(Conflict(b2.name, b1.name, conflicted_files) )
                                    conflicts.setdefault(b2.name, []).append(Conflict(b1.name, b2.name, conflicted_files))
        self._reset()
        return conflicts


class ConflictHtmlPublisher:
    def __init__(self, conflicts):
        self._conflicts = conflicts

    def _files_to_list(self, files):
        ul = []
        if files:
            ul.append("<ul>")
            for f in files:
                ul.append("<li>{0}</li>".format(f))
            ul.append("</ul>")
        return "\n".join(ul)


    def export(self, filename):
        html = []
        styles = '''<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg .tg-yw4l{vertical-align:top}
</style>'''

        html.append("<html>")
        html.append(styles)
        html.append('<body><table class="tg">')
        html.append('<tr><th>branch</th><th>branch</th><th>files</th></tr>')
        for k in sorted(self._conflicts.keys()):
                values = self._conflicts[k];
                v = values[0]
                rowspan = ''
                if len(values) > 1:
                    rowspan=' rowspan="{0}"'.format(len(values))
                html.append('<tr><td{0}>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(rowspan, k, v.branch1_name, self._files_to_list(v.conflicted_paths)))                
                for v1 in values[1:]:
                    html.append('<tr><td>{0}</td><td>{1}</td></tr>'.format(v1.branch1_name, self._files_to_list(v1.conflicted_paths)))

        html.append('</table>')
        html.append('</body></html>')

        file = open(filename,"w") 
        file.write("\n".join(html))
        file.close()


              
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',stream=sys.stdout, level=logging.INFO)

    ignore_patterns = ['.*CHANGELOG','.*pubspec.yaml']

    repository_path = sys.argv[1]
    html_report = sys.argv[2]
    
    logging.info("Starting for '{0}'".format(repository_path))

    detector = ConflictDetector(repository_path, ignore_patterns)

    detector.pullAllBrachesLocaly()

    conflicts = detector.get_merge_conflicts()

    ConflictHtmlPublisher(conflicts).export(html_report)
    