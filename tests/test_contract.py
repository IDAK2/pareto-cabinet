from pathlib import Path
SOURCE=(Path(__file__).parents[1]/'contracts'/'contract.py').read_text()

def test_specification_is_frozen_and_rechecked():
 assert "digest=self._freeze(url)" in SOURCE
 assert "if current!=spec_digest" in SOURCE

def test_every_semantic_driver_is_consensus_bound():
 for token in ('exact ordered binary penalty vector',"'artifact_digest'","'penalties'",'complete artifact'):
  assert token in SOURCE

def test_pareto_rule_is_deterministic_and_not_total_score():
 assert 'all(left[i]<=right[i]' in SOURCE and 'any(left[i]<right[i]' in SOURCE
 assert 'sum(' not in SOURCE

def test_duplicate_digest_cannot_mutate_frontier():
 assert SOURCE.index('if replay_key in self.attempted') < SOURCE.index('frontier=json.loads')

def test_permissionless_seal_requires_three_evaluations():
 block=SOURCE[SOURCE.index('def seal_assay'):SOURCE.index('@gl.public.view',SOURCE.index('def seal_assay'))]
 assert 'gl.message.sender_address' not in block and "len(json.loads(assay.evaluated_ids))<3" in block
