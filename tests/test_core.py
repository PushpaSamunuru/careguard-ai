from careguard.core import classify, verify

def test_agency_classification():
    assert classify('Agency called about caregiver shift') == 'agency_call'

def test_mismatch_flag():
    result = verify('Agency called about staffing', 'Monthly check-in completed')
    assert result['category_mismatch'] and result['review_required']

def test_unknown_requires_review():
    assert verify('Silent line', 'No information')['review_required']

def test_supported_category():
    assert not verify('Monthly check-in completed', 'Monthly check-in completed')['review_required']
