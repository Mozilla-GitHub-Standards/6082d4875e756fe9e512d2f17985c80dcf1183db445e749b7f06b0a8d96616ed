APPNAME = server-reg
DEPS = server-core, server-node-assignment
VIRTUALENV = virtualenv
NOSE = bin/nosetests -s --with-xunit
TESTS = syncreg/tests
PYTHON = bin/python
BUILDAPP = bin/buildapp
BUILDRPMS = bin/buildrpms
PYPI = http://pypi.python.org/simple
PYPIOPTIONS = -i $(PYPI)
CHANNEL = dev
RPM_CHANNEL = prod
INSTALL = bin/pip install
INSTALLOPTIONS = -U -i $(PYPI)

ifdef PYPIEXTRAS
	PYPIOPTIONS += -e $(PYPIEXTRAS)
	INSTALLOPTIONS += -f $(PYPIEXTRAS)
endif

ifdef PYPISTRICT
	PYPIOPTIONS += -s
	ifdef PYPIEXTRAS
		HOST = `python -c "import urlparse; print urlparse.urlparse('$(PYPI)')[1] + ',' + urlparse.urlparse('$(PYPIEXTRAS)')[1]"`

	else
		HOST = `python -c "import urlparse; print urlparse.urlparse('$(PYPI)')[1]"`
	endif

endif

INSTALL += $(INSTALLOPTIONS)



.PHONY: all build test build_rpms mach

all:	build

build:
	$(VIRTUALENV) --no-site-packages --distribute .
	$(INSTALL) MoPyTools
	$(INSTALL) nose
	$(INSTALL) WebTest
	$(BUILDAPP) -c $(CHANNEL) $(PYPIOPTIONS) $(DEPS)

update:
	$(BUILDAPP) -c $(CHANNEL) $(PYPIOPTIONS) $(DEPS)

test:
	$(NOSE) $(TESTS)

build_rpms:
	$(BUILDRPMS) -c $(RPM_CHANNEL) $(DEPS)

mach: build build_rpms
	mach clean
	mach yum install python26 python26-setuptools
	cd rpms; wget http://mrepo.mozilla.org/mrepo/5-x86_64/RPMS.mozilla-services/gunicorn-0.11.2-1moz.x86_64.rpm
	cd rpms; wget http://mrepo.mozilla.org/mrepo/5-x86_64/RPMS.mozilla/nginx-0.7.65-4.x86_64.rpm
	mach yum install rpms/*
	mach chroot python2.6 -m syncreg.run
