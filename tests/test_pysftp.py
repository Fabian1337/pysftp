def test_success():
	assert True

def test_failure():
	assert False == False
	
	
import pysftp

def test_connection_good():
    sftp = pysftp.Connection('calypso.delasco.pri')
    sftp.close()
    
    
def test_connection_bad():
    try:
        sftp = pysftp.Connection('no-existy.delasco.pri')
        assert False
    except:
        assert True

