from ntds.miners import Miner

@Miner.register
class DNGrep(Miner):
    _name_ = "DNGrep"
    _desc_ = "DN grepper"
    @classmethod
    def create_arg_subparser(cls, parser):
        parser.add_argument("--cn", help="Look for objects with given CN and print their DN")
    
    def run(self, options):

        col = options.db.open_table()

        def find_dn(r):
            if not r:
                return ""
            cn = r.get("cn") or r.get("name")
            if cn is None or cn=="$ROOT_OBJECT$":
                return ""
            r2 = col.find_one({"RecId":r["ParentRecId"]})
            return find_dn(r2)+"."+cn
    
        c = col.find({"cn":options.cn})
        for r in c:
            print "=>",r.get("cn"),find_dn(r)
            
