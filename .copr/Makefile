srpm:
	dnf -y install git make gcc flex bison bzip2 dwarves xz rpm-build python3-pyyaml rust rust-src bindgen rustfmt
	git config user.email "fedora@leemhuis.info"
	git config user.name "Thorsten Leemhuis"

		git branch -f arkify-upstream-stable-7.2 HEAD || true

	make NO_CONFIGCHECKS=1 DIST=.fc41 UPSTREAMBUILD_GIT_ONLY=0 dist-srpm || \
	make NO_CONFIGCHECKS=1 DIST=.fc41 UPSTREAMBUILD_GIT_ONLY=0 LOCALVERSION=.local dist-srpm

	mv redhat/rpm/SRPMS/*.src.rpm $(outdir)
