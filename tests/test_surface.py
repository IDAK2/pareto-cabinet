from pathlib import Path
HTML=(Path(__file__).parents[1]/'docs'/'index.html').read_text(encoding='utf-8')
def test_complete_specimen_lifecycle():
 for token in ('OPEN CABINET','INSERT SPECIMEN','SEAL CATALOGUE','FINALIZED','open_assay','insert_candidate','seal_assay','get_assay'):
  assert token in HTML
def test_cabinet_identity():
 for token in ('specimen-drawer','frontier-wire','assay-bench','constraint-lamp'):
  assert token in HTML
 assert 'chair-ring' not in HTML and '<table' not in HTML and '<pre' not in HTML
