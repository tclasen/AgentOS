import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from validate_bundle import parse
from route_demo import route

class Routing(unittest.TestCase):
    def test_graph(self):
        nodes,comps,errors=parse()
        self.assertEqual(errors,[])
        self.assertGreaterEqual(len(comps),20)
    def test_minimal(self):
        chosen,_,_=route(set())
        self.assertEqual(len(chosen),10)
        self.assertNotIn('/components/telemetry.md',chosen)
    def test_git_does_not_force_unrelated_ledger(self):
        chosen,_,_=route({'remote_git_delivery'})
        self.assertIn('/components/git-delivery.md',chosen)
        self.assertIn('/components/effect-reconciliation.md',chosen)
        self.assertNotIn('/components/durable-handoff.md',chosen)
        self.assertNotIn('/components/work-ledger.md',chosen)
    def test_parallel_requires_ownership(self):
        chosen,_,_=route({'parallel_workers'})
        for name in ('parallel-coordination','work-ledger','resource-budgets'):
            self.assertIn('/components/'+name+'.md',chosen)
    def test_brownfield_multirepo_no_scheduling(self):
        chosen,_,_=route({'existing_agent_system','multiple_repositories','sensitive_data'})
        for name in ('brownfield-migration','multi-repo','information-boundaries'):
            self.assertIn('/components/'+name+'.md',chosen)
        self.assertNotIn('/components/scheduling.md',chosen)

if __name__=='__main__':unittest.main()
